import streamlit as st
import pandas as pd
import base64
import altair as alt
import pg8000 as psycopg
from dotenv import load_dotenv
load_dotenv()
import os
import google.generativeai as genai

# Load environment variables
host = os.getenv("host")
database = os.getenv("database")
user = os.getenv("user")
password = os.getenv("password")
port = os.getenv("port")


def connect_to_postgres():
    try:
        conn = psycopg.connect(
            host= host,
            database= database,
            user= user,
            password= password,
            port= port  # Thường là 5432
        )
        return conn
    except Exception as e:
        st.error(f"Error connecting to PostgreSQL: {e}")
        return None

connect = connect_to_postgres()

genai.configure(api_key = os.getenv("key"))
model = genai.GenerativeModel("gemini-1.5-flash")

base_prompt = ['''
    You are an expert in converting English questions to postgres SQL query!\n
    The SQL database has the name "weather" and the table name is "weather_data".\n
    CREATE TABLE weather_data (
    province VARCHAR(255),
    max FLOAT,
    min FLOAT,
    wind FLOAT,
    wind_d VARCHAR(50),
    rain FLOAT,
    humidi FLOAT,
    cloud FLOAT,
    pressure FLOAT,
    date DATE,
    year INT,
    month INT,
    is_outlier BOOLEAN,
    region VARCHAR(255)
    );

    max - maximum temperature in Celsius, in a day
    min - minimum temperature in Celsius, in a day
    
    When I ask a question for the max in Hanoi in 2021, the SQL query should be "SELECT year, max(max) as "max_temperature_of_year" FROM weather_data WHERE province = 'Hanoi' AND year = 2021" Group by year.\n
    When I ask a question for the min during the year 2021, the SQL query should be "SELECT date, province, min FROM weather_data WHERE year = 2021".\n
               
    For example:\n
    EX1: if the question is "What is the maximum temperature in Hanoi? in 2021", 
    the SQL query should be "SELECT year, max(max) FROM weather_data WHERE province = 'Hanoi' AND year = 2021".\n
    EX2: if the question is "What is the minimum temperature in Hanoi in 2021?",
    the SQL query should be "SELECT year, min(min) FROM weather_data WHERE province = 'Hanoi' AND year = 2021".\n
    EX3: if the question is "What is the humidi in Hanoi in 2021?",
    the SQL query should be "SELECT date, humidi FROM weather_data WHERE province = 'Hanoi' AND year = 2021".\n
    
    If using any function in the SQL query, please define the name of the column name in the output.\n
    Also, the Postgres code should not have ``` in the beginning or end and the Postgres word in the output.\n
    The following are some questions that you can ask:
''',
'''
    You are an expert in converting English questions to python code!\n
    The python code is use for visualization data from the dataframe.\n
    Using the library "matplotlib", "seaborn" to visualize the data in python 3.13.\n

    For example:\n
    EX1: if the question is "Visualize line chart for the humidity in Hanoi in 2021",\n
    # Vẽ biểu đồ\n
    plt.figure(figsize=(15, 6))\n
    sns.lineplot(data=df, x="Date", y="Humidity", color="blue")\n

    # Thiết lập tiêu đề và nhãn\n
    plt.title("Độ ẩm tại Hà Nội trong năm 2021", fontsize=16)\n
    plt.xlabel("Ngày", fontsize=12)\n
    plt.ylabel("Độ ẩm (%)", fontsize=12)\n
    plt.xticks(rotation=45)\n
    plt.grid(True, linestyle="--", alpha=0.6)\n

    # Hiển thị biểu đồ\n
    plt.tight_layout()\n
    plt.show()\n

    Also, the Postgres code should not have ``` in the beginning or end and python word in the output.\n
    The df is the dataframe that you get from the SQL query so you don't have to define the df.\n
    Give me an only one block of code to visualize the data.\n
    Also, the plot should be saved in the output.png file.\n
    The following are some questions that you can ask:
'''
,
'''
    You are an expert in reading an image and analyzing the data in the image!\n
    With an analysis request, you can analyze the data in the image and provide the result.\n
    The image is a photo of the instruments in the lab.\n
''',
'''
Bạn là một chuyên gia trong việc đọc hình ảnh và phân tích dữ liệu trong hình ảnh!\n
Với một yêu cầu phân tích, bạn có thể phân tích dữ liệu trong hình ảnh và cung cấp kết quả.\n 
Hình ảnh là một bức ảnh của các dụng cụ trong phòng thí nghiệm.\n
'''
]

st.markdown("""
    <style>
        .custom-container {
            background-color: lightblue;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px 0 rgba(0, 0, 0, 0.1);
            width: 1200px;
        }
    </style>
""", unsafe_allow_html=True)


# Function to load Google  Gemini modek and provide sql query as response
def get_gemini_query_response(question,prompt):
    response=model.generate_content([prompt[0],question])
    return response.text

def get_gemini_vis_response(question,prompt, df):
    # Get the description of the dataframe
    df_desc = ""
    df_desc = df_desc + "The dataframe has the following columns: \n"
    df_desc = df.columns.to_list()
    df_desc = ",".join(df_desc)
    df_desc = df_desc + "\n Visualize by a chart following the question: \n"
    # Get the question and prompt
    question = question + "\n" + df_desc
    print(question)

    response=model.generate_content([prompt[1],question])
    return response.text

def get_gemini_analysis_response(question,prompt, df, language="English"):
    myfile = genai.upload_file("output.png")
    print(f"{myfile=}")

    # chuyển df từ dạng bảng thành dạng chuỗi
    df = df.to_string()
    
    question = question + "\n" + df
    if language == "Vietnamese":
        return model.generate_content(
            [myfile, prompt[3], question]
        ).text
    else:
        return model.generate_content(
            [myfile, prompt[2], question]
        ).text



embebbed_html = '''
<iframe src="https://public.tableau.com/views/FINALPROJECT_17344580550510/Dashboard1?:showVizHome=no&:embed=true" width="1554" height="1319" style="align-items: flex-start;"></iframe>
'''

def dashboard(html):
    custom_css = """
    <style>
    .st-emotion-cache-bm2z3a {
        display: flex;
        flex-direction: column;
        width: 100%;
        overflow: auto;
        -webkit-box-align: flex-start !important;
        align-items: flex-start !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.markdown(html, unsafe_allow_html=True)


def load_data(path):
    data = pd.read_csv(path)
    return data

option = ''
with st.sidebar:
    st.title('Menu')
    st.write('Choose the option you want to see')
    option = st.radio('Select an option', ['Dashboard', 'Chatbot', 'Analysis'], index=0)

if option == 'Dashboard':
    dashboard(embebbed_html)
elif option == 'Analysis':
    st.header('This is the chart that you\'ve required before')
    # Đọc ảnh và chuyển đổi thành base64
    image_path = 'output.png'
    with open(image_path, 'rb') as image_file:
        image_data = image_file.read()

    # Chuyển đổi ảnh thành base64
    encoded_image = base64.b64encode(image_data).decode('utf-8')
    st.markdown(f'<img src="data:image/png;base64,{encoded_image}" alt="plot" style="width: 100%; height: auto;">', unsafe_allow_html=True)
    # thêm nút lựa chọn giữa tiếng việt và tiếng anh
    st.write("Choose the language")
    language = st.radio("Language", ["English", "Vietnamese"], index=0)
    analysis_request = st.text_input("Analysis request: ", key="input_analysis")
    submit_analysis = st.button("Analysis")
    df = pd.read_csv("output.csv")
    
    if submit_analysis:

        if language == "Vietnamese":
            response = get_gemini_analysis_response(analysis_request,base_prompt, df, language="Vietnamese")
            st.markdown(f"Response: {response}")
        else:
            response = get_gemini_analysis_response(analysis_request,base_prompt, df, language="English")
            st.markdown(f"Response: {response}")


else:
    with st.container(border=True):
        st.header('Chatbot for querying data')
        question=st.text_input("Query request: ",key="input")
        
        submit=st.button("Query")
        if submit:
            response = get_gemini_query_response(question,base_prompt)
            # Display the response by markdown
            st.markdown(f"Response: {response}")
            if connect is not None:
                try:
                    cursor = connect.cursor()
                    cursor.execute(response)
                    result = cursor.fetchall()
                    # Nếu null thì thông báo
                    if len(result) == 0:
                        st.warning("No data found")
                    else:
                        # cho vào dataframe để hiển thị
                        df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
                        print(df)
                        st.write(df)
                        # ghi ra file csv
                        df.to_csv("output.csv", index=False)
                except Exception as e:
                    st.error(f"Error executing the query: {e}")
            else:
                st.error("No connection to the database")

    with st.container(border=True):
        input_vis = st.text_input("Visualize request: ", key="input_vis")
        submit_vis = st.button("Visualize")

        # đọc file csv
        df = pd.read_csv("output.csv")
        # chuyển df thành dataframe
        df = pd.DataFrame(df)
        # visualize the data
        # st.write("Visualization")
        vis = get_gemini_vis_response(input_vis,base_prompt, df)
        st.write(vis)
        
        # khử ``` và python
        vis = vis.replace("```","")
        vis = vis.replace("python","")
        # thêm vào cuối đoạn code để hiển thị biểu đồ st.pyplot()
        vis = vis + "\nst.pyplot()"
        try:
            exec(vis)
            # lưu biểu đồ ra file png
            
        except Exception as e:
            st.error(f"Error executing the query: {e}")


        

