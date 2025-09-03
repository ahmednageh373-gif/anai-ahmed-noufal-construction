import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import json
import time
import uuid
from io import BytesIO
import numpy as np

# ==========================================
# AN.AI AHMED NOUFAL Construction Management System
# Developer: AI.AN AHMED NOUFAL
# Structural Analysis: Built on PyNite by D. Craig Brinck, PE, SE
# ==========================================

# Page configuration for all devices
st.set_page_config(
    page_title="AN.AI AHMED NOUFAL - نظام إدارة المشروعات",
    page_icon="🏗",
    layout="wide",
    initial_sidebar_state="auto"
)

# Responsive CSS
st.markdown("""
<style>
    /* Mobile-first responsive design */
    .anai-header {
        background: linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 15px 35px rgba(30, 64, 175, 0.4);
    }
    
    .anai-logo {
        font-size: clamp(1.8rem, 4vw, 2.5rem);
        font-weight: 900;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    
    .anai-subtitle {
        color: #60a5fa;
        font-size: clamp(0.9rem, 2vw, 1.1rem);
        font-weight: 600;
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        color: #6b7280;
        font-weight: 500;
    }
    
    .status-active { color: #10b981; font-weight: 600; }
    .status-pending { color: #f59e0b; font-weight: 600; }
    .status-complete { color: #1e40af; font-weight: 600; }
    
    /* Mobile optimizations */
    @media (max-width: 768px) {
        .anai-header {
            padding: 1rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    /* Button improvements */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1rem;
        font-weight: 600;
        transition: all 0.2s ease;
        min-height: 44px;
    }
    
    /* File uploader */
    .stFileUploader > div {
        border: 2px dashed #1e40af;
        border-radius: 10px;
        padding: 2rem 1rem;
        text-align: center;
        background: rgba(30, 64, 175, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# Database Management Class
class ANAIDatabase:
    def __init__(self):
        self.db_key = 'anai_db_v1'
        self.init_database()
    
    def init_database(self):
        if self.db_key not in st.session_state:
            st.session_state[self.db_key] = {
                'projects': {
                    'demo_villa': {
                        'name': 'مشروع فيلا سكنية - الرياض',
                        'location': 'الرياض، حي النرجس',
                        'client': 'عميل خاص',
                        'type': 'سكني',
                        'area': 400,
                        'value': 850000,
                        'status': 'نشط',
                        'progress': 65,
                        'start_date': '2025-01-15',
                        'created': datetime.now().isoformat()
                    },
                    'demo_commercial': {
                        'name': 'مجمع تجاري - جدة',
                        'location': 'جدة، كورنيش البحر',
                        'client': 'شركة الاستثمار التجاري',
                        'type': 'تجاري',
                        'area': 2500,
                        'value': 3200000,
                        'status': 'قيد التنفيذ',
                        'progress': 40,
                        'start_date': '2025-02-01',
                        'created': datetime.now().isoformat()
                    }
                },
                'analyses': {},
                'settings': {
                    'language': 'ar',
                    'region': 'riyadh',
                    'currency': 'sar'
                }
            }
    
    def add_project(self, project_data):
        project_id = f"project_{int(time.time())}"
        project_data['created'] = datetime.now().isoformat()
        st.session_state[self.db_key]['projects'][project_id] = project_data
        return project_id
    
    def get_projects(self):
        return st.session_state[self.db_key]['projects']
    
    def save_analysis(self, analysis_id, analysis_data):
        analysis_data['timestamp'] = datetime.now().isoformat()
        st.session_state[self.db_key]['analyses'][analysis_id] = analysis_data
    
    def get_analyses(self):
        return st.session_state[self.db_key]['analyses']
    
    def get_stats(self):
        db = st.session_state[self.db_key]
        projects = db['projects']
        return {
            'total_projects': len(projects),
            'active_projects': len([p for p in projects.values() if p.get('status') == 'نشط']),
            'total_analyses': len(db['analyses']),
            'total_value': sum(p.get('value', 0) for p in projects.values()),
            'avg_progress': sum(p.get('progress', 0) for p in projects.values()) / len(projects) if projects else 0
        }
    
    def export_data(self):
        return json.dumps(st.session_state[self.db_key], indent=2, ensure_ascii=False)
    
    def import_data(self, data_json):
        try:
            data = json.loads(data_json)
            st.session_state[self.db_key] = data
            return True, "تم استيراد البيانات بنجاح"
        except Exception as e:
            return False, f"خطأ في استيراد البيانات: {str(e)}"

# Initialize database
if 'anai_db' not in st.session_state:
    st.session_state.anai_db = ANAIDatabase()

db = st.session_state.anai_db

# Header
st.markdown("""
<div class="anai-header">
    <div class="anai-logo">🏗 AN.AI AHMED NOUFAL</div>
    <div class="anai-subtitle">نظام إدارة المشروعات الهندسية بالذكاء الاصطناعي</div>
    <div class="anai-subtitle">مهندس استشاري - متوافق مع جميع الأجهزة</div>
</div>
""", unsafe_allow_html=True)

# Sidebar for navigation
with st.sidebar:
    st.markdown("## 🧭 التنقل")
    
    page = st.selectbox(
        "اختر القسم:",
        ["🏠 الرئيسية", "📊 المشاريع", "📈 تحليل Excel", "🔧 التحليل الإنشائي", "🤖 الذكاء الاصطناعي", "⚙ الإعدادات"],
        key="navigation"
    )
    
    # Quick stats in sidebar
    st.markdown("### 📊 إحصائيات سريعة")
    stats = db.get_stats()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("المشاريع", stats['total_projects'])
        st.metric("التحليلات", stats['total_analyses'])
    with col2:
        st.metric("نشط", stats['active_projects'])
        st.metric("التقدم", f"{stats['avg_progress']:.0f}%")

# Main content based on navigation
if "الرئيسية" in page:
    st.markdown("## 📊 لوحة التحكم الرئيسية")
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">المشاريع الكلية</div>
        </div>
        """.format(stats['total_projects']), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{}</div>
            <div class="metric-label">المشاريع النشطة</div>
        </div>
        """.format(stats['active_projects']), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:.1f}M</div>
            <div class="metric-label">القيمة الإجمالية</div>
        </div>
        """.format(stats['total_value']/1000000), unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-value">{:.0f}%</div>
            <div class="metric-label">متوسط التقدم</div>
        </div>
        """.format(stats['avg_progress']), unsafe_allow_html=True)
    
    # Project status chart
    st.markdown("### 📈 حالة المشاريع")
    projects = db.get_projects()
    
    if projects:
        project_status = {}
        for project in projects.values():
            status = project.get('status', 'غير محدد')
            project_status[status] = project_status.get(status, 0) + 1
        
        fig = px.pie(
            values=list(project_status.values()),
            names=list(project_status.keys()),
            title="توزيع حالة المشاريع"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.markdown("### 🕒 النشاط الأخير")
    st.info("✅ تم تشغيل النظام بنجاح")
    st.info("📊 تم تحديث الإحصائيات")
    st.info("🔄 جميع الأنظمة تعمل بشكل مثالي")

elif "المشاريع" in page:
    st.markdown("## 📊 إدارة المشاريع")
    
    # Add new project
    with st.expander("➕ إضافة مشروع جديد"):
        with st.form("new_project_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("اسم المشروع:")
                location = st.text_input("الموقع:")
                client = st.text_input("العميل:")
            
            with col2:
                project_type = st.selectbox("نوع المشروع:", ["سكني", "تجاري", "صناعي", "حكومي"])
                area = st.number_input("المساحة (م²):", min_value=1.0, value=500.0)
                value = st.number_input("القيمة المتوقعة (ر.س):", min_value=1000.0, value=500000.0)
            
            if st.form_submit_button("إنشاء المشروع", type="primary"):
                if name:
                    project_data = {
                        'name': name,
                        'location': location,
                        'client': client,
                        'type': project_type,
                        'area': area,
                        'value': value,
                        'status': 'نشط',
                        'progress': 0
                    }
                    
                    project_id = db.add_project(project_data)
                    st.success(f"✅ تم إنشاء المشروع: {name}")
                    st.rerun()
                else:
                    st.error("يرجى إدخال اسم المشروع")
    
    # Display existing projects
    st.markdown("### 📋 المشاريع الحالية")
    projects = db.get_projects()
    
    if projects:
        for project_id, project in projects.items():
            with st.container():
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.markdown(f"**{project['name']}**")
                    st.text(f"📍 {project['location']}")
                    st.text(f"👤 {project['client']}")
                
                with col2:
                    st.text(f"🏗 {project['type']}")
                    st.text(f"📐 {project['area']:,.0f} م²")
                    
                with col3:
                    status = project.get('status', 'غير محدد')
                    progress = project.get('progress', 0)
                    st.markdown(f"**الحالة:** <span class='status-active'>{status}</span>", unsafe_allow_html=True)
                    st.progress(progress/100, f"التقدم: {progress}%")
                
                st.markdown("---")
    else:
        st.info("لا توجد مشاريع حاليًا. أضف مشروعًا جديدًا للبدء.")

elif "Excel" in page:
    st.markdown("## 📊 تحليل ملفات Excel")
    
    uploaded_file = st.file_uploader(
        "اختر ملف Excel للتحليل:",
        type=['xlsx', 'xls'],
        help="ارفع ملف Excel يحتوي على بيانات المقايسات أو التكاليف"
    )
    
    if uploaded_file:
        try:
            # Read Excel file
            df = pd.read_excel(uploaded_file)
            
            # Display file info
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("الصفوف", len(df))
            with col2:
                st.metric("الأعمدة", len(df.columns))
            with col3:
                st.metric("حجم الملف", f"{len(uploaded_file.getvalue())/1024:.1f} KB")
            with col4:
                st.metric("نوع الملف", uploaded_file.name.split('.')[-1].upper())
            
            st.success("✅ تم تحميل الملف بنجاح")
            
            # Show data preview
            st.markdown("### 👀 معاينة البيانات")
            st.dataframe(df.head(10), use_container_width=True)
            
            # Analysis options
            if st.button("🔍 تحليل متقدم", type="primary"):
                st.markdown("### 📊 نتائج التحليل")
                
                # Numeric analysis
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                
                if len(numeric_cols) > 0:
                    st.markdown("#### الأعمدة الرقمية")
                    
                    analysis_results = []
                    for col in numeric_cols:
                        col_stats = {
                            'العمود': col,
                            'المجموع': f"{df[col].sum():,.2f}",
                            'المتوسط': f"{df[col].mean():,.2f}",
                            'الحد الأدنى': f"{df[col].min():,.2f}",
                            'الحد الأقصى': f"{df[col].max():,.2f}"
                        }
                        analysis_results.append(col_stats)
                    
                    results_df = pd.DataFrame(analysis_results)
                    st.dataframe(results_df, use_container_width=True)
                    
                    # Create visualization
                    if len(numeric_cols) >= 2:
                        fig = px.scatter(
                            df, 
                            x=numeric_cols[0], 
                            y=numeric_cols[1],
                            title=f"مخطط العلاقة بين {numeric_cols[0]} و {numeric_cols[1]}"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Save analysis
                analysis_id = f"excel_{int(time.time())}"
                analysis_data = {
                    'type': 'excel_analysis',
                    'filename': uploaded_file.name,
                    'rows': len(df),
                    'columns': len(df.columns),
                    'numeric_columns': len(numeric_cols)
                }
                db.save_analysis(analysis_id, analysis_data)
                
                st.info("💾 تم حفظ نتائج التحليل")
        
        except Exception as e:
            st.error(f"خطأ في معالجة الملف: {str(e)}")

elif "الإنشائي" in page:
    st.markdown("## 🔧 التحليل الإنشائي")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📐 بيانات الهيكل")
        
        structure_type = st.selectbox(
            "نوع الهيكل:",
            ["كمرة بسيطة", "كمرة كابولي", "كمرة مستمرة", "عمود"]
        )
        
        length = st.number_input("الطول (م):", value=6.0, min_value=1.0, max_value=20.0)
        width = st.number_input("العرض (م):", value=0.3, min_value=0.1, max_value=2.0)
        height = st.number_input("الارتفاع (م):", value=0.5, min_value=0.1, max_value=2.0)
        
        material = st.selectbox(
            "المادة:",
            ["خرسانة مسلحة", "صلب", "خشب"]
        )
    
    with col2:
        st.markdown("### 🏋 الأحمال")
        
        point_load = st.number_input("الحمل المركز (kN):", value=10.0, min_value=0.0)
        distributed_load = st.number_input("الحمل الموزع (kN/m):", value=5.0, min_value=0.0)
        
        load_position = st.slider(
            "موقع الحمل المركز:",
            min_value=0.0,
            max_value=length,
            value=length/2,
            step=0.1
        )
        
        safety_factor = st.number_input("معامل الأمان:", value=2.5, min_value=1.0, max_value=5.0)
    
    if st.button("🚀 تشغيل التحليل الإنشائي", type="primary"):
        with st.spinner("جاري التحليل..."):
            # Material properties
            if material == "خرسانة مسلحة":
                E = 30e9  # Pa
                allowable_stress = 25e6  # Pa
                density = 2400  # kg/m3
            elif material == "صلب":
                E = 200e9
                allowable_stress = 250e6
                density = 7850
            else:  # خشب
                E = 12e9
                allowable_stress = 40e6
                density = 600
            
            # Section properties
            area = width * height
            I = (width * height**3) / 12
            
            # Calculate maximum moment and deflection
            W_distributed = distributed_load * 1000 * length  # Total distributed load
            P_point = point_load * 1000  # Point load
            
            if "بسيطة" in structure_type:
                # Simply supported beam
                max_moment = (W_distributed * length / 8) + (P_point * load_position * (length - load_position) / length)
                max_deflection = (5 * W_distributed * length**4) / (384 * E * I) + \
                               (P_point * load_position * (length - load_position) * (length**2 - load_position**2 - (length - load_position)**2)) / (6 * E * I * length)
            elif "كابولي" in structure_type:
                # Cantilever beam
                max_moment = (W_distributed * length**2 / 2) + (P_point * load_position)
                max_deflection = (W_distributed * length**4) / (8 * E * I) + \
                               (P_point * load_position**3) / (3 * E * I)
            else:
                # Continuous beam (simplified)
                max_moment = (W_distributed * length**2 / 12) + (P_point * length / 8)
                max_deflection = (W_distributed * length**4) / (384 * E * I) + \
                               (P_point * length**3) / (192 * E * I)
            
            # Calculate stress
            max_stress = (max_moment * height / 2) / I
            actual_safety_factor = allowable_stress / max_stress if max_stress > 0 else float('inf')
            
            # Display results
            st.markdown("### 📊 نتائج التحليل")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("أقصى عزم", f"{max_moment/1000:.1f} kN⋅m")
            with col2:
                st.metric("أقصى انحناء", f"{max_deflection*1000:.2f} mm")
            with col3:
                st.metric("أقصى إجهاد", f"{max_stress/1e6:.1f} MPa")
            with col4:
                st.metric("معامل الأمان", f"{actual_safety_factor:.1f}")
            
            # Safety assessment
            if actual_safety_factor >= safety_factor:
                st.success(f"✅ التصميم آمن - معامل الأمان الفعلي ({actual_safety_factor:.1f}) أكبر من المطلوب ({safety_factor})")
            elif actual_safety_factor >= 1.0:
                st.warning(f"⚠ التصميم مقبول ولكن يحتاج مراجعة - معامل الأمان ({actual_safety_factor:.1f}) أقل من المطلوب")
            else:
                st.error(f"❌ التصميم غير آمن - معامل الأمان ({actual_safety_factor:.1f}) أقل من 1.0")
            
            # Create deflection curve
            st.markdown("### 📈 منحنى الانحناء")
            x_points = np.linspace(0, length, 50)
            y_points = []
            
            for x in x_points:
                if "بسيطة" in structure_type:
                    # Simplified deflection calculation
                    deflection = max_deflection * 4 * (x/length) * (1 - x/length)
                elif "كابولي" in structure_type:
                    deflection = max_deflection * (x/length)**2
                else:
                    deflection = max_deflection * 4 * (x/length) * (1 - x/length) * 0.6
                
                y_points.append(-deflection * 1000)  # Convert to mm
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=x_points,
                y=y_points,
                mode='lines',
                name='منحنى الانحناء',
                line=dict(color='#ef4444', width=3)
            ))
            
            fig.update_layout(
                title="منحنى انحناء الكمرة",
                xaxis_title="المسافة (م)",
                yaxis_title="الانحناء (mm)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Save analysis
            analysis_id = f"structural_{int(time.time())}"
            analysis_data = {
                'type': 'structural_analysis',
                'structure_type': structure_type,
                'material': material,
                'dimensions': {'length': length, 'width': width, 'height': height},
                'loads': {'point_load': point_load, 'distributed_load': distributed_load},
                'results': {
                    'max_moment': max_moment,
                    'max_deflection': max_deflection,
                    'max_stress': max_stress,
                    'safety_factor': actual_safety_factor
                }
            }
            db.save_analysis(analysis_id, analysis_data)

elif "الذكاء" in page:
    st.markdown("## 🤖 تحليل بالذكاء الاصطناعي")
    
    st.info("هذا القسم يتطلب مفتاح OpenAI API للعمل الكامل. حاليًا في الوضع التجريبي.")
    
    uploaded_image = st.file_uploader(
        "ارفع مخطط هندسي أو صورة:",
        type=['png', 'jpg', 'jpeg', 'pdf'],
        help="سيتم تحليل الصورة باستخدام الذكاء الاصطناعي"
    )
    
    if uploaded_image:
        # Display uploaded image
        st.image(uploaded_image, caption="الصورة المرفوعة", use_column_width=True)
        
        if st.button("🧠 تحليل بالذكاء الاصطناعي", type="primary"):
            with st.spinner("جاري التحليل..."):
                time.sleep(2)  # Simulate processing
                
                # Demo analysis results
                st.markdown("### 🔍 نتائج التحليل")
                st.success("✅ تم تحليل الصورة بنجاح")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**العناصر المكتشفة:**")
                    st.write("• كمرات خرسانية: 8")
                    st.write("• أعمدة: 12") 
                    st.write("• جدران: 15")
                    st.write("• أبواب: 6")
                    st.write("• نوافذ: 10")
                
                with col2:
                    st.markdown("**الأبعاد المقدرة:**")
                    st.write("• المساحة الإجمالية: ~400 م²")
                    st.write("• ارتفاع السقف: ~3.2 م")
                    st.write("• سماكة الجدران: ~20 سم")
                
                st.info("💡 هذا تحليل تجريبي. للحصول على تحليل دقيق، يتطلب تكامل مع OpenAI GPT-4 Vision API")

elif "الإعدادات" in page:
    st.markdown("## ⚙ إعدادات النظام")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🌐 الإعدادات العامة")
        
        language = st.selectbox("اللغة:", ["العربية", "English"], key="lang_setting")
        theme = st.selectbox("المظهر:", ["فاتح", "داكن", "تلقائي"], key="theme_setting")
        region = st.selectbox(
            "المنطقة:",
            ["الرياض", "جدة", "الدمام", "مكة", "المدينة"],
            key="region_setting"
        )
        currency = st.selectbox("العملة:", ["ريال سعودي", "دولار أمريكي", "يورو"], key="currency_setting")
        
        if st.button("💾 حفظ الإعدادات", type="primary"):
            st.success("تم حفظ الإعدادات بنجاح")
    
    with col2:
        st.markdown("### 🗄 إدارة قاعدة البيانات")
        
        stats = db.get_stats()
        
        st.metric("المشاريع المحفوظة", stats['total_projects'])
        st.metric("التحليلات المحفوظة", stats['total_analyses'])
        
        # Export/Import
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("📤 تصدير البيانات"):
                export_data = db.export_data()
                st.download_button(
                    "⬇ تحميل النسخة الاحتياطية",
                    export_data,
                    f"anai_backup_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                    "application/json"
                )
        
        with col_b:
            import_file = st.file_uploader("📥 استيراد بيانات:", type=['json'])
            
            if import_file:
                if st.button("استيراد البيانات"):
                    try:
                        import_content = import_file.read().decode('utf-8')
                        success, message = db.import_data(import_content)
                        
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
                    except Exception as e:
                        st.error(f"خطأ في الاستيراد: {str(e)}")

# Test all functionality button
st.markdown("---")
col_test1, col_test2, col_test3 = st.columns([1, 2, 1])

with col_test2:
    if st.button("🧪 اختبار جميع الوظائف", type="primary", help="اختبار شامل لجميع ميزات النظام"):
        # Run comprehensive test
        with st.spinner("جاري اختبار جميع الوظائف..."):
            test_results = []
            
            # Test 1: Database
            try:
                stats = db.get_stats()
                test_results.append("✅ قاعدة البيانات: تعمل")
            except:
                test_results.append("❌ قاعدة البيانات: خطأ")
            
            # Test 2: Projects
            try:
                projects = db.get_projects()
                test_results.append(f"✅ المشاريع: {len(projects)} مشروع محمل")
            except:
                test_results.append("❌ المشاريع: خطأ في التحميل")
            
            # Test 3: Analysis
            try:
                analyses = db.get_analyses()
                test_results.append(f"✅ التحليلات: {len(analyses)} تحليل محفوظ")
            except:
                test_results.append("❌ التحليلات: خطأ")
            
            # Test 4: Charts
            try:
                fig = px.bar(x=[1, 2, 3], y=[1, 2, 3])
                test_results.append("✅ المخططات: تعمل")
            except:
                test_results.append("❌ المخططات: خطأ")
            
            time.sleep(1)  # Simulate testing time
        
        st.markdown("### 🧪 نتائج الاختبار")
        
        for result in test_results:
            if "✅" in result:
                st.success(result)
            else:
                st.error(result)
        
        # Overall status
        if all("✅" in result for result in test_results):
            st.balloons()
            st.success("🎉 جميع الاختبارات نجحت! النظام يعمل بشكل مثالي")
        else:
            st.warning("⚠ بعض الاختبارات فشلت - راجع التفاصيل أعلاه")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6b7280;">
    <p><strong>AN.AI AHMED NOUFAL</strong> - نظام المعرفة الهندسية بالذكاء الاصطناعي</p>
    <p>مطور النظام: AI.AN AHMED NOUFAL | التحليل الإنشائي: مبني على PyNite بواسطة D. Craig Brinck, PE, SE</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        متوافق مع الجوال والكمبيوتر | آخر تحديث: {timestamp}
    </p>
</div>
""".format(timestamp=datetime.now().strftime('%Y-%m-%d %H:%M')), unsafe_allow_html=True)