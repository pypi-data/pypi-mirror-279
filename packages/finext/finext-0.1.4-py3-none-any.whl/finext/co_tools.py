from finlab import data
import finlab
import pickle
import os
import plotly.express as px
from finlab.backtest import sim
from finlab.tools.event_study import create_factor_data
import tqdm
import numpy as np 
import pandas as pd
from finlab.dataframe import FinlabDataFrame
import cufflinks as cf
from sklearn.linear_model import LinearRegression
from datetime import datetime
from IPython.display import display, HTML
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import fitz  # PyMuPDF
# import df_type

db_path = "/home/sb0487/trade/finlab/finlab_db" #資料儲存路徑



"""
程式碼傷眼滲入


"""
#若未來相關函式增多再開發
class cofindf(FinlabDataFrame):
    @property
    def pr(self):
        # 計算每行的有效值數量
        valid_counts = self.count(axis=1)
        valid_counts = valid_counts.replace(0, np.nan)
        rank_df = self.rank(axis=1, ascending=True, na_option='keep')
        pr_df = rank_df.div(valid_counts, axis=0) * 100
        return pr_df


#載入區----------------------------------------------------------------------------------------------------------------

class Codata():
    def __init__(self ,df_type = "findf", db_path = "",force_download = False ):
        # super().__init__()
        self.df_type = df_type
        self.db_path = db_path
        data.set_storage(data.FileStorage(db_path))
        data.use_local_data_only = False
        data.force_cloud_download = force_download
        

    
    def get_file_path(self,file_name): 
        return os.path.join(self.db_path, file_name.replace(":", "#") + ".pickle")

    
    def get_update_time(self,filename):
        if os.path.exists(self.get_file_path(filename)):
            modification_time = os.path.getmtime(self.get_file_path(filename))
            last_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(modification_time))
            print(f"最後更新時間: {last_modified}, {[filename]}")
        else:
            print("檔案不存在,請柬查路徑")

    
    def ouput_type_df(self,file_df):
        if self.df_type == "findf":
            type_df = file_df
        elif self.df_type == "cudf":
            import cudf
            type_df = cudf.DataFrame(file_df)
        elif self.df_type == "sparkdf":
            from pyspark.sql import SparkSession
            spark = SparkSession.builder.appName("Pandas to Spark DataFrame").getOrCreate()
            type_df = spark.createDataFrame(file_df)
        return type_df


    def get(self, file_name, force_download = False ):
        if not os.path.isdir(self.db_path):
            raise OSError("資料夾路徑錯誤")

        if force_download == True:
            data.force_cloud_download = True 
            type_df = data.get(file_name)
            data.force_cloud_download = False
        else:
            type_df = data.get(file_name)
            
        #選擇df輸出型態
        type_df = self.ouput_type_df(type_df)
        self.get_update_time(file_name)
        return type_df

    # @staticmethod
    # def get_update_time(filename):
    #     data.get_update_time(filename)  # 调用 data 类的 get_update_time 方法

    

#產業區----------------------------------------------------------------------------------------------------------------
    
    #把category拆成主分類與細分類
    def get_industry_pro(self):
        industry = self.get('security_industry_themes').dropna()
        def extract_majcategory(category_list):
            matching_categories = set([category.split(':')[0] for category in eval(category_list) if ':' in category])
            return str(list(matching_categories))
        
        def extract_subcategory(category_list):
            matching_categories = [category.split(':')[-1] for category in eval(category_list) if ':' in category]
            return str(matching_categories)
        
        # 应用自定义函数到 DataFrame 的每一行
        industry['maj_category'] = industry['category'].apply(extract_majcategory)
        industry['sub_category'] = industry['category'].apply(extract_subcategory)
        
        return industry

    
    def show_industry(self):
        industry = self.get_industry_pro()
        sub_category_counts_df = pd.DataFrame(industry['sub_category'].apply(eval).explode('sub_category').value_counts()).reset_index()
        maj_category_counts_df = pd.DataFrame(industry['maj_category'].apply(eval).explode('maj_category').value_counts()).reset_index()
        
        industry["maj_category"] = industry["maj_category"].apply(eval)
        industry["sub_category"] = industry["sub_category"].apply(eval)
        industry_explode = industry.explode('maj_category').explode('sub_category')
        industry_explode["count"] = 1
        
        fig = px.treemap(industry_explode, path=[px.Constant("台股產業總總覽"), "maj_category", "sub_category","name"], values='count')
        fig.update_layout(
            margin=dict(t=1, l=1, r=1, b=1)
        )
        
        fig.show()
        return maj_category_counts_df,sub_category_counts_df
    
    def filter_industry(self,file_df, keyword_list, category_type = "maj_category", remove_or_add="remove", exact_or_fuzzy="fuzzy"):
        industry_pro = self.get_industry_pro()
        
        if exact_or_fuzzy == "fuzzy":
            if remove_or_add == "remove":
                
                file_filtered_df = (file_df
                    .loc[:, ~file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) & set(keyword_list)))]['stock_id']
                        .tolist())]
                )
           
            elif remove_or_add == "add":
                file_filtered_df = (file_df
                    .loc[:, file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) & set(keyword_list)))]['stock_id']
                        .tolist())]
                )
    
        
        if exact_or_fuzzy == "exact":
            if remove_or_add == "remove": # 完全一樣才移除
                
                file_filtered_df = (file_df
                    .loc[:, ~file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) == set(keyword_list)))]['stock_id']
                        .tolist())]
                )
    
            elif remove_or_add == "add": # 完全一樣才加入
                file_filtered_df = (file_df
                    .loc[:, file_df.columns.isin(
                        industry_pro[industry_pro[category_type]
                        .apply(lambda x: bool(set(eval(x)) == set(keyword_list)))]['stock_id']
                        .tolist())]
                )
        
        return file_filtered_df



    
    
    #把category拆成主分類與細分類
    def get_industry_pro(self):
        industry = self.get('security_industry_themes').dropna()
        def extract_majcategory(category_list):
            matching_categories = set([category.split(':')[0] for category in eval(category_list) if ':' in category])
            return str(list(matching_categories))
        
        def extract_subcategory(category_list):
            matching_categories = [category.split(':')[-1] for category in eval(category_list) if ':' in category]
            return str(matching_categories)
        
        # 应用自定义函数到 DataFrame 的每一行
        industry['maj_category'] = industry['category'].apply(extract_majcategory)
        industry['sub_category'] = industry['category'].apply(extract_subcategory)
        
        return industry

#便利工具區----------------------------------------------------------------------------------------------------------------

        # def month_forward_sell(self,forward_days = 1):
        #     exits_df = self.get('price:收盤價')<0
        #     def update_row(row):
        #         if row.name in self.monthly_revenue.index:
        #             return True
        #         else:
        #             return row
        
        #     rev_date = exits_df.apply(update_row, axis=1)
        #     rev_date_shifted = rev_date.shift(-1)
        #     for i in range(1,forward_days+1):
        #         rev_date_shifted_n = rev_date.shift(-i)
        #         rev_date_shifted = rev_date_shifted  | rev_date_shifted_n
                
        return rev_date_shifted
    
    #把日資料轉成月資料(營收發布截止日),他們有說之後會改成電子檔上傳日
    def day_to_month(self,file_df):
        monthly_index_df = FinlabDataFrame(index=self.get("monthly_revenue:當月營收").index)
        file_df  = monthly_index_df.join(file_df, how='left')
        return file_df

    def to_day(self,file_df):
        monthly_index_df = FinlabDataFrame(index=self.get('price:收盤價').index)
        file_df  = monthly_index_df.join(file_df, how='left')
        return file_df
    
    #轉為日資料並藉由資料異動時間點保留財報發布日資訊(index_str_to_date會向下填滿)    
    def q_to_day(self,file_df):
        file_df =file_df.index_str_to_date()
        file_df =file_df.where(file_df.ne(file_df.shift()), np.nan)
        day_index_df = FinlabDataFrame(index=self.get('price:收盤價').index)
        c = pd.concat([file_df,day_index_df])
        file_df = FinlabDataFrame(c[~c.index.duplicated()].sort_index())
        return file_df
        
    def get_pr(self, file_df):
        # 計算每行的有效值數量
        valid_counts = file_df.count(axis=1)
        valid_counts[valid_counts == 0] = np.nan
        rank_df = file_df.rank(axis=1, ascending=True, na_option='keep')
        pr_df = rank_df.div(valid_counts, axis=0) * 100
        
        return pr_df

    def display_report_statis(self, file_df):
        max_year_compound_ret = (1 + file_df["return"].mean()) ** (240 / file_df["period"].mean())
    
        html_content = """
        <sorry style="font-size: larger;">交易統計</sorry>
        <ul>
          <li>交易筆數: {}</li>
          <li>平均報酬率: {:.3f}</li>
          <li>平均MDD: {:.3f}</li>
          <li>報酬率標準差: {:.3f}</li>
          <li>平均持有期間(交易日): {:.3f}</li>
          <li>平均處於獲利天數: {:.3f}</li>
          <li>最大年化複利報酬: {:.3f}</li>
        </ul>
        """.format(len(file_df),
                   file_df["return"].mean(),
                   file_df["mdd"].mean(),
                   file_df["return"].std(),
                   file_df["period"].mean(),
                   file_df["pdays"].mean(),
                   max_year_compound_ret)
        
        display(HTML(html_content))
#爬蟲區----------------------------------------------------------------------------------------------------------------------
    
    #爬年報
    def crawl_annual_report_(self,year,symbol,save_dir,sleep = 2):
        #init
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式
        year = str(year)
        symbol = str(symbol)
        
    
        d = webdriver.Chrome(options=chrome_options)
        d.maximize_window()
    
        try:
            while True:
                d.get(f'https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={symbol}&year={year}&mtype=F&dtype=F04&') 
                time.sleep(sleep)
                
                page_content = d.page_source
                if "查詢過量" in page_content:
                    print(f"當前股票為{symbol},查詢過量，被證交所檔下，休息10秒")
                    time.sleep(10)
                    continue  
                else:
                    break  # 如果没有查詢過量，退出循环
    
            pdf_link = d.find_element(By.XPATH, "//a[contains(@href, 'javascript:readfile2') and contains(@href, 'F04')]")
            pdf_link.click()
            time.sleep(sleep)
        
            # 切換分頁
            all_tabs = d.window_handles
            d.switch_to.window(all_tabs[1])
            time.sleep(sleep)
    
            
            # 找到pdf連結,注意此連結為不定時浮動
            pdf_link2 = d.find_element(By.XPATH, "//a[contains(@href, '.pdf')]")
            pdf_url = pdf_link2.get_attribute('href')
        
            
            # 建構dir(若無),保存pdf
            os.makedirs(save_dir, exist_ok=True)
            file_name = f"{year}_{symbol}.pdf" 
            file_path = os.path.join(save_dir, file_name)
            
            # 下载 PDF 文件并保存
            response = requests.get(pdf_url)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"PDF 文件已保存到: {file_path}")
            failed_symbol =None
            
        except ModuleNotFoundError as e:
            print(f"Module not found error: {e}")
            
        except NameError as e:
            print(f"Name not defined error: {e}") 
            
        except Exception as e:
            print(f"{symbol}_{year}年年報未找到")
            failed_symbol = symbol
            
        finally:
            d.quit()
            
        return failed_symbol
    #爬年報,多個
    def crawl_annual_reports(self,year,stock_list,save_dir,sleep = 2):
        failed_list = list(filter(None, (self.crawl_annual_report_(year, x, save_dir, sleep) for x in stock_list)))
        return failed_list
        
    #爬季報
    def crawl_quarterly_report_(self,year,quarter,symbol,save_dir,sleep = 2):
        
        #init
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # 無頭模式
        year = str(year)
        symbol = str(symbol)
        format_quarter = "0"+str(quarter)
        ad = str(int(year)+1911)
        # 初始化Chrome瀏覽器
        # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        
    
        d = webdriver.Chrome(options=chrome_options)
        d.maximize_window()
    
        try:
            while True:
                d.get(f'https://doc.twse.com.tw/server-java/t57sb01?step=1&colorchg=1&co_id={symbol}&year={year}&seamon=&mtype=A&dtype=AI1&') 
                time.sleep(sleep)
                
                page_content = d.page_source
                if "查詢過量" in page_content:
                    print(f"當前股票為{symbol},查詢過量，被證交所檔下，休息10秒")
                    time.sleep(10)
                    continue  
                else:
                    break  # 如果没有查詢過量，退出循环
           
            pdf_name = f"{ad}{format_quarter}_{symbol}_AI1.pdf"
            pdf_link = d.find_element(By.XPATH, f"//a[contains(@href, 'javascript:readfile2') and contains(@href,'{pdf_name}')]")
            pdf_link.click()
            time.sleep(sleep)
        
            # 切換分頁
            all_tabs = d.window_handles
            d.switch_to.window(all_tabs[1])
            time.sleep(sleep)
    
            # 找到pdf連結,注意此連結為不定時浮動
            pdf_link2 = d.find_element(By.XPATH, "//a[contains(@href, '.pdf')]")
            pdf_url = pdf_link2.get_attribute('href')
        
            
            # 建構dir(若無),保存pdf
            os.makedirs(save_dir, exist_ok=True)
            file_name = f"{year}_Q{quarter}_{symbol}.pdf" 
            file_path = os.path.join(save_dir, file_name)
            
            # 下载 PDF 文件并保存
            response = requests.get(pdf_url)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(f"PDF 文件已保存到: {file_path}")
            failed_symbol =None
            
        except ModuleNotFoundError as e:
            print(f"Module not found error: {e}")
            
        except NameError as e:
            print(f"Name not defined error: {e}") 
        
        except:
            print(f"{symbol}_{year}_Q{quarter}季報未找到")
            failed_symbol = symbol
            
        finally:
            d.quit()
        return failed_symbol
    #爬季報,多個
    def crawl_quarterly_reports(self,year,quarter,stock_list,save_dir,sleep = 2):
        failed_list = list(filter(None, (self.crawl_quarterly_report_(year,quarter, x, save_dir, sleep) for x in stock_list)))
        return failed_list


    #用save_dir抓下來的檔案與全部的股票代號清單all_stock_list比較,找出尚未下載的pdf
    def get_undownloaded_stocks(self,save_dir,all_stock_list):
        download_stock_list = [f.split('.')[0][-4:] for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
        result = [elem for elem in all_stock_list if elem not in download_stock_list]
        return result

#讀檔pdf區----------------------------------------------------------------------------------------------------------------------
    
    #用spark分散式讀取
    def load_pdf_spark(self,stock_list,pdf_path,memory = "5g"):
        from pyspark.sql import SparkSession
        
        # 起 Spark
        spark = SparkSession.builder.appName("Read PDFs with Spark")\
        .config("spark.driver.memory", memory)\
        .config("spark.driver.maxResultSize", memory)\
        .getOrCreate() # 內存大小
    
        def process_pdf(filename):
            if filename.endswith('.pdf'):
                #stock_symbol = filename.split('_')[1].split('.')[0] # 分割,取出股票代耗
                stock_symbol = filename.split('.')[0][-4:]
                if stock_symbol in stock_list: 
                    file_path = os.path.join(pdf_path, filename)
                    content = "".join(page.get_text() for page in fitz.open(file_path)) #打開pdf, 逐行讀取並合併
                    return stock_symbol, content
    
        # 使用 Spark 讀取每個 PDF 文件
        pdf_contents = spark.sparkContext.parallelize(os.listdir(pdf_path)).map(process_pdf).filter(lambda x: x).collect()
        
        # 將結果轉換為 Pandas DataFrame
        pdf_df = pd.DataFrame(pdf_contents, columns=["Stock Symbol", "PDF Content"]).set_index("Stock Symbol")
        return pdf_df

    #單線程讀取
    def load_pdf(self,stock_list, pdf_path):
        def process_pdf(filename):
            if filename.endswith('.pdf'):
                stock_symbol = filename.split('.')[0][-4:]
                if stock_symbol in stock_list:
                    file_path = os.path.join(pdf_path, filename)
                    content = "".join(page.get_text() for page in fitz.open(file_path))  
                    return stock_symbol, content
        
        pdf_contents = [process_pdf(filename) for filename in os.listdir(pdf_path) if filename.endswith('.pdf')]
        pdf_contents = [item for item in pdf_contents if item is not None]
        
        # 将结果转换为 Pandas DataFrame
        pdf_df = pd.DataFrame(pdf_contents, columns=["Stock Symbol", "PDF Content"]).set_index("Stock Symbol")
        return pdf_df













