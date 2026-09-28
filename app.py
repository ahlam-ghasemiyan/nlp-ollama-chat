import streamlit as st
import ollama
import base64

# تنظیمات اولیه صفحه
st.set_page_config(page_title="دستیار هوشمند NLP", page_icon="😉")

# --- تابع برای تنظیم پس‌زمینه و استایل‌های CSS ---
def set_custom_style(image_file):
    # 1. خواندن و انکود تصویر پس‌زمینه
    try:
        with open(image_file, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        background_image_style = f"""
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        """
    except FileNotFoundError:
        background_image_style = ""
        st.warning(f"⚠️ فایل تصویر '{image_file}' پیدا نشد.")

    # 2. تزریق کل CSS ها
    st.markdown(
        f"""
        <style>
        /* تنظیم تصویر پس‌زمینه اصلی */
        .stApp {{
            {background_image_style}
        }}

        /* 1. تغییر رنگ سایدبار به سبز ملایم */
        [data-testid="stSidebar"] {{
            background-color: rgba(212, 237, 218, 0.95) !important;
            border-right: 2px solid #c3e6cb;
        }}

        /* 2. تغییر رنگ تمام تیترها و متن‌های صفحه به مشکی */
        h1, h2, h3, .stCaption, p, label, .stMarkdown, .stSuccess {{
            color: black !important;
        }}
        
        /* 3. تنظیمات باکس ورودی متن (Text Area) */
        .stTextArea textarea {{
             background-color: rgba(255, 255, 255, 0.9) !important;
             color: black !important;
             caret-color: black;
             border: 1px solid #ced4da;
             font-weight: 500;
        }}
        
        /* رنگ متن راهنما (Placeholder) داخل باکس */
        .stTextArea textarea::placeholder {{
            color: #333333 !important;
            opacity: 1;
        }}

        /* 4. تنظیمات دکمه ارسال (بسیار مهم: سفید کردن متن) */
        
        /* خود دکمه */
        .stButton > button {{
            background-color: #001f3f !important; /* پس‌زمینه سرمه‌ای */
            border: none;
            padding: 10px 24px;
            font-weight: bold;
        }}

        /* این دستور تمام متن‌های داخل دکمه را مجبور می‌کند سفید شوند */
        .stButton > button p, .stButton > button div, .stButton > button span {{
            color: #FFFFFF !important;
        }}
        
        /* حالت هاور (موس روی دکمه) */
        .stButton > button:hover {{
             background-color: #000000 !important; /* پس‌زمینه مشکی */
             border: 1px solid white; /* یک حاشیه سفید نازک برای زیبایی */
        }}
        
        /* متن در حالت هاور هم سفید بماند */
        .stButton > button:hover p, .stButton > button:hover div {{
             color: #FFFFFF !important;
        }}

        </style>
        """,
        unsafe_allow_html=True
    )

# اعمال استایل‌ها (مطمئن شوید عکس 11.png کنار فایل است)
set_custom_style('11.png')

# --- شروع برنامه اصلی ---

# عنوان برنامه
st.title("🦙 چت با هوش مصنوعی (لوکال)")
st.caption("اجرا شده با مدل Mistral جهت پروژه NLP")

# --- سایدبار (تنظیمات) ---
st.sidebar.header("تنظیمات")
model_name = "mistral"

# انتخاب نقش هوش مصنوعی
mode = st.sidebar.selectbox(
    "نقش هوش مصنوعی را انتخاب کنید:",
    ("پزشک (Physician)", "تحلیل احساسات (Sentiment)", "پیشنهاد محصول", "چت آزاد")
)

# --- منطق انتخاب نقش ---
system_instruction = ""
if mode == "پزشک (Physician)":
    system_instruction = "Consider that you are a physician. The user will tell you symptoms, tell them what to do. Keep it short and professional."
elif mode == "تحلیل احساسات (Sentiment)":
    system_instruction = "Classify the sentiment of the provided text strictly as either 'Positive' or 'Negative'. Do not add any explanation."
elif mode == "پیشنهاد محصول":
    system_instruction = "Act as a shopping assistant. Recommend a complementary product based on what the user has bought previously."
else:
    system_instruction = "You are a helpful and polite AI assistant designed for an NLP course demonstration."

# --- محیط اصلی ---
user_input = st.text_area("متن ورودی:", height=150, placeholder="مثلاً: من سردرد و تب دارم...")

# دکمه ارسال
if st.button("ارسال به هوش مصنوعی 🚀"):
    if user_input:
        with st.spinner("درحال پردازش..."):
            try:
                # ارسال پیام به اولاما
                response = ollama.chat(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": "user", "content": user_input}
                    ]
                )
                
                # نمایش نتیجه
                st.markdown(f"""
                    <div style='
                        background-color: rgba(212, 237, 218, 0.95); 
                        padding: 20px; 
                        border-radius: 10px; 
                        color: black; 
                        border: 2px solid #c3e6cb;
                        margin-top: 20px;
                        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
                    '>
                        <h4 style='margin-top:0; color:#155724;'>پاسخ مدل:</h4>
                        {response['message']['content']}
                    </div>
                    """, unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"خطا در ارتباط با Ollama: {e}")
                st.info("نکته: مطمئن شوید که نرم‌افزار Ollama در حال اجراست.")
    else:
        st.warning("لطفاً ابتدا متنی بنویسید.")

# پاورقی
st.markdown("---")
st.markdown("<h5 style='text-align: center; color: black;'>😉 ساخته شده برای ارایه درس پردازش زبان های طبیعی توسط مهندس قاسمیان </h5>", unsafe_allow_html=True)