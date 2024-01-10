from flask import Flask, render_template, request, session , redirect
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.secret_key = 'ket'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:HwzsqdcjsodCQ5Qs@db.djaqphyiavlljtllpurl.supabase.co:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)    

class User(db.Model):
    __tablename__ = 'user-system' 
    userid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
      
headings =("SchemeID", "SchemeName", "EligibilityCriteria", "Details", "Benefits", "StartDate", "EndDate", "Department")
dataW = (
     (1, 'Women''s Education Empowerment', 'Women pursuing higher education', 'Provides scholarships and financial assistance', 'Tuition fee coverage, mentorship programs', '2024-06-01', '2025-05-31', 'Ministry of Education'),

    (2, 'Maternal Healthcare Support', 'Pregnant women and new mothers', 'Ensures access to quality maternal healthcare services', 'Prenatal care, postnatal care, vaccinations', '2024-07-01', '2024-12-31', 'Ministry of Health'),

    (3, 'Women''s Entrepreneurship Development', 'Aspiring women entrepreneurs', 'Facilitates skill development and business support', 'Training programs, startup grants, mentorship', '2024-08-01', '2025-07-31', 'Ministry of Small and Medium Enterprises'),

    (4, 'Gender Equality in the Workplace', 'Working women facing discrimination', 'Promotes gender equality and addresses workplace bias', 'Equal pay initiatives, anti-discrimination training', '2024-09-01', '2025-08-31', 'Ministry of Labor'),

    (5, 'Rural Women Development Fund', 'Rural women involved in agriculture or cottage industries', 'Supports rural women in economic activities', 'Agricultural training, financial aid, infrastructure development', '2024-10-01', '2025-05-31', 'Ministry of Rural Development'),

    (6, 'Women''s Health Awareness Program', 'All women in the community', 'Promotes health awareness and preventive care', 'Health screenings, workshops, informational campaigns', '2024-11-01', '2024-11-30', 'Ministry of Health'),

    (7, 'Skill Development for Single Mothers', 'Single mothers and caregivers', 'Provides training for employable skills', 'Vocational training, job placement assistance', '2025-01-01', '2025-01-31', 'Ministry of Women and Child Development'),

    (8, 'Women in Science Scholarship', 'Female students pursuing STEM fields', 'Encourages women to pursue careers in science', 'Scholarship funds, mentorship by women scientists', '2025-02-01', '2025-02-28', 'Ministry of Science and Technology'),

    (9, 'Domestic Violence Support Helpline', 'Women facing domestic violence', 'Provides a helpline for counseling and support', 'Crisis intervention, legal aid referrals', '2025-03-01', '2025-03-31', 'Ministry of Social Justice'),

    (10, 'Women''s Empowerment in Agriculture', 'Women involved in agriculture', 'Promotes sustainable farming practices and market access', 'Training, agricultural resources, market linkages', '2025-04-01', '2025-04-30', 'Ministry of Agriculture'),

    (11, 'Financial Literacy for Women', 'Women in low-income communities', 'Educates women on financial management and entrepreneurship', 'Financial literacy workshops, access to microfinance', '2025-05-01', '2025-05-31', 'Ministry of Finance'),

    (12, 'Sports Scholarship for Women', 'Female athletes pursuing sports at the national level', 'Supports talented women in sports', 'Scholarship funds, specialized training', '2025-06-01', '2025-06-30', 'Ministry of Youth Affairs and Sports'),

    (13, 'Urban Women Housing Subsidy', 'Urban women from economically weaker sections', 'Provides financial assistance for housing', 'Subsidized housing loans, affordable housing projects', '2025-07-01', '2025-07-31', 'Ministry of Urban Development'),

    (14, 'Artisan Empowerment Program', 'Women engaged in traditional crafts and artisanal work', 'Preserves and promotes traditional crafts', 'Skill development, market access, cultural events', '2025-08-01', '2025-08-31', 'Ministry of Culture'),

    (15, 'Women''s Mental Health Initiative', 'Women dealing with mental health challenges', 'Addresses mental health issues and provides support', 'Counseling services, awareness campaigns', '2025-09-01', '2025-09-30', 'Ministry of Health')
)
dataT = (
     (1, 'Transgender Education Scholarship', 'Transgender individuals pursuing higher education', 'Provides financial assistance for tuition and living expenses', 'Scholarship funds, mentorship programs', '2024-06-01', '2025-05-31', 'Ministry of Education'),

    (2, 'Healthcare Equality Program', 'All transgender individuals', 'Ensures access to gender-affirming healthcare services', 'Medical consultations, hormone therapy, gender-affirming surgeries', '2024-07-01', '2024-12-31', 'Ministry of Health'),

    (3, 'Transgender Employment Support', 'Unemployed transgender individuals', 'Assists in finding employment opportunities and skill development', 'Job placement services, vocational training programs', '2024-08-01', '2025-07-31', 'Ministry of Labor'),

    (4, 'Housing Rights for Transgender Individuals', 'Transgender individuals facing housing discrimination or homelessness', 'Provides housing assistance and legal support', 'Temporary shelters, rental assistance, legal aid', '2024-09-01', '2025-08-31', 'Ministry of Social Justice'),

    (5, 'Transgender Cultural Empowerment Grant', 'Transgender individuals involved in promoting cultural awareness', 'Supports cultural projects and events that celebrate transgender diversity', 'Grant funding for events, workshops, and artistic projects', '2024-10-01', '2025-05-31', 'Ministry of Culture'),

    (6, 'Transgender Mental Health Support', 'Transgender individuals dealing with mental health challenges', 'Addresses mental health issues and provides counseling services', 'Therapy sessions, support groups, awareness campaigns', '2024-11-01', '2024-11-30', 'Ministry of Health'),

    (7, 'Transgender Entrepreneurship Development', 'Transgender individuals interested in starting businesses', 'Facilitates skill development and business support', 'Training programs, startup grants, mentorship', '2025-01-01', '2025-01-31', 'Ministry of Small and Medium Enterprises'),

    (8, 'Legal Aid for Transgender Rights', 'Transgender individuals facing legal challenges', 'Provides legal assistance for issues related to transgender rights', 'Legal consultations, representation in court', '2025-02-01', '2025-02-28', 'Ministry of Law'),

    (9, 'Transgender Sports Inclusion Program', 'Transgender athletes aspiring to compete', 'Promotes inclusion in sports for transgender individuals', 'Training facilities, participation in sporting events', '2025-03-01', '2025-03-31', 'Ministry of Youth Affairs and Sports'),

    (10, 'Transgender Skill Development in Arts', 'Transgender individuals interested in arts and culture', 'Supports skill development in various artistic disciplines', 'Workshops, exhibitions, cultural events', '2025-04-01', '2025-04-30', 'Ministry of Culture'),

    (11, 'Transgender Community Health Clinics', 'All transgender individuals', 'Establishes community health clinics for transgender-specific healthcare', 'Primary care, counseling services, outreach programs', '2025-05-01', '2025-05-31', 'Ministry of Health'),

    (12, 'Transgender Employment Equality Initiative', 'Transgender individuals in the workforce', 'Promotes equal employment opportunities and workplace inclusion', 'Employment workshops, diversity training for companies', '2025-06-01', '2025-06-30', 'Ministry of Labor'),

    (13, 'Transgender Housing Assistance Program', 'Transgender individuals facing housing challenges', 'Provides financial aid for housing and rental assistance', 'Temporary housing support, legal aid for housing issues', '2025-07-01', '2025-07-31', 'Ministry of Social Justice'),

    (14, 'Transgender Youth Education Outreach', 'Transgender youth in schools and colleges', 'Creates awareness and support systems for transgender students', 'Educational workshops, counseling services', '2025-08-01', '2025-08-31', 'Ministry of Education'),

    (15, 'Transgender Arts and Culture Festival', 'All transgender individuals with an interest in arts and culture', 'Celebrates transgender creativity and diversity through a cultural festival', 'Art exhibitions, performances, workshops', '2025-09-01', '2025-09-30', 'Ministry of Culture')
)
dataS = (
    (1, 'Education for All', 'Students pursuing primary, secondary, or higher education', 'Provides financial assistance and support for educational expenses', 'Scholarship funds, educational resources, mentorship programs', '2024-06-01', '2025-05-31', 'Ministry of Education'),

    (2, 'STEM Scholarship Program', 'Students pursuing Science, Technology, Engineering, and Mathematics (STEM) fields', 'Encourages and supports students in STEM disciplines', 'Scholarship funds, research opportunities, industry connections', '2024-07-01', '2024-12-31', 'Ministry of Science and Technology'),

    (3, 'Skill Development for Students', 'Students seeking vocational training and skill development', 'Facilitates training programs for employable skills', 'Vocational training, job placement assistance, career counseling', '2024-08-01', '2025-07-31', 'Ministry of Skill Development'),

    (4, 'Digital Literacy Initiative', 'Students aiming to enhance digital skills', 'Promotes digital literacy and technological proficiency', 'Training in digital technologies, access to digital resources', '2024-09-01', '2025-08-31', 'Ministry of Information Technology'),

    (5, 'Environmental Awareness Campaign', 'Students interested in environmental conservation', 'Creates awareness and promotes sustainable practices', 'Educational workshops, tree planting campaigns', '2024-10-01', '2025-05-31', 'Ministry of Environment'),

    (6, 'Student Health and Wellness Program', 'All students in educational institutions', 'Focuses on promoting physical and mental health among students', 'Health check-ups, counseling services, wellness activities', '2024-11-01', '2024-11-30', 'Ministry of Health'),

    (7, 'Art and Culture Scholarships', 'Students pursuing degrees in arts and culture', 'Supports artistic and cultural endeavors of students', 'Scholarship funds, exhibition opportunities', '2025-01-01', '2025-01-31', 'Ministry of Culture'),

    (8, 'Sports Development Initiative', 'Students with a passion for sports', 'Promotes sports participation and development', 'Sports training, participation in tournaments', '2025-02-01', '2025-02-28', 'Ministry of Youth Affairs and Sports'),

    (9, 'Community Service Learning', 'Students interested in community service', 'Encourages students to engage in community-oriented projects', 'Community service projects, volunteer opportunities', '2025-03-01', '2025-03-31', 'Ministry of Social Welfare'),

    (10, 'Entrepreneurship Development for Students', 'Aspiring student entrepreneurs', 'Facilitates entrepreneurship training and support', 'Startup grants, mentorship programs', '2025-04-01', '2025-04-30', 'Ministry of Small and Medium Enterprises'),

    (11, 'International Exchange Program', 'Students seeking international exposure', 'Provides opportunities for studying abroad and cultural exchange', 'Study abroad programs, cross-cultural experiences', '2025-05-01', '2025-05-31', 'Ministry of Foreign Affairs'),

    (12, 'Innovation and Research Grants', 'Students engaged in innovative research projects', 'Supports student-led research and innovation', 'Research grants, access to laboratories', '2025-06-01', '2025-06-30', 'Ministry of Research and Development'),

    (13, 'Literary and Writing Competitions', 'Students interested in literature and writing', 'Promotes literary skills and creativity', 'Literary competitions, publication opportunities', '2025-07-01', '2025-07-31', 'Ministry of Education'),

    (14, 'Diversity and Inclusion Awareness', 'Students advocating for diversity and inclusion', 'Raises awareness and fosters inclusivity on campuses', 'Workshops, events, awareness campaigns', '2025-08-01', '2025-08-31', 'Ministry of Social Justice'),

    (15, 'Technology Innovation Challenge', 'Students interested in technological innovation', 'Encourages students to develop innovative technological solutions', 'Technology challenges, recognition for innovations', '2025-09-01', '2025-09-30', 'Ministry of Science and Technology')
)
dataF = (
    (1, 'Crop Insurance Program', 'Farmers with cultivated land', 'Provides insurance coverage for crops', 'Compensation for crop losses due to natural disasters', '2024-06-01', '2025-05-31', 'Ministry of Agriculture'),

    (2, 'Modern Agricultural Equipment Subsidy', 'Farmers in need of agricultural machinery', 'Subsidizes the purchase of modern farming equipment', 'Reduced cost of agricultural machinery', '2024-07-01', '2024-12-31', 'Ministry of Agriculture'),

    (3, 'Soil Health Improvement Initiative', 'Farmers interested in soil health', 'Promotes soil health and fertility improvement', 'Free soil testing, subsidies for soil amendments', '2024-08-01', '2025-07-31', 'Ministry of Agriculture'),

    (4, 'Drought-Resistant Crop Development', 'Farmers in drought-prone regions', 'Encourages cultivation of drought-resistant crops', 'Seeds and support for drought-resistant crop varieties', '2024-09-01', '2025-08-31', 'Ministry of Agriculture'),

    (5, 'Organic Farming Promotion', 'Farmers transitioning to organic farming', 'Promotes and supports organic farming practices', 'Training, certification support, marketing assistance', '2024-10-01', '2025-05-31', 'Ministry of Agriculture'),

    (6, 'Water Conservation Grants', 'Farmers implementing water conservation practices', 'Supports initiatives for water-efficient farming', 'Financial assistance for water conservation projects', '2024-11-01', '2024-11-30', 'Ministry of Agriculture'),

    (7, 'Market Linkage and Export Support', 'Farmers looking to expand market reach', 'Facilitates access to markets and export opportunities', 'Market linkages, export subsidies', '2025-01-01', '2025-01-31', 'Ministry of Commerce'),

    (8, 'Livestock Health and Vaccination Program', 'Farmers with livestock', 'Ensures the health and vaccination of livestock', 'Free veterinary services, vaccination campaigns', '2025-02-01', '2025-02-28', 'Ministry of Agriculture'),

    (9, 'Agricultural Extension Services', 'Farmers seeking expert advice', 'Provides agricultural extension services', 'Access to agricultural experts, workshops, training', '2025-03-01', '2025-03-31', 'Ministry of Agriculture'),

    (10, 'Farmers'' Market Infrastructure Development', 'Farmers involved in direct selling', 'Develops infrastructure for farmers'' markets', 'Market infrastructure, storage facilities', '2025-04-01', '2025-04-30', 'Ministry of Agriculture'),

    (11, 'Farmers'' Training and Skill Development', 'Farmers interested in skill enhancement', 'Enhances farmers'' skills in various agricultural practices', 'Training programs, skill development workshops', '2025-05-01', '2025-05-31', 'Ministry of Agriculture'),

    (12, 'Climate-Resilient Agriculture', 'Farmers in climate-vulnerable areas', 'Promotes climate-resilient agricultural practices', 'Seeds, technologies, and practices for climate resilience', '2025-06-01', '2025-06-30', 'Ministry of Agriculture'),

    (13, 'Horticulture Development Scheme', 'Farmers involved in horticulture', 'Supports the development of horticultural practices', 'Training, subsidies for horticultural crops', '2025-07-01', '2025-07-31', 'Ministry of Agriculture'),

    (14, 'Farm Pond Construction Program', 'Farmers interested in water storage', 'Encourages construction of farm ponds for water storage', 'Financial assistance for farm pond construction', '2025-08-01', '2025-08-31', 'Ministry of Agriculture'),

    (15, 'Integrated Pest Management', 'Farmers dealing with pest issues', 'Promotes sustainable pest management practices', 'Training, organic pest control methods', '2025-09-01', '2025-09-30', 'Ministry of Agriculture')
)

@app.route("/")
def home():
    return render_template("login.html")

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(name=name, password=password).first()
        if user:
            session['loggedin'] = True
            session['userid'] = user.userid
            session['name'] = user.name
            session['email'] = user.email
            mesage = 'Logged in successfully!'
            return render_template('index.html', mesage=mesage)
        else:
            mesage = 'Please enter you correct credentials if registered, if not please register'
    return render_template("login.html", mesage=mesage)

@app.route('/register.html', methods=['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        user_name = request.form['name']
        password = request.form['password']
        email = request.form['email']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            mesage = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address!'
        elif not user_name or not password or not email:
            mesage = 'Please fill out the form!'
        else:
            new_user = User(name=user_name, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            mesage = 'You have successfully registered!'
    elif request.method == 'POST':
        mesage = 'Please fill out the form!'
    return render_template('register.html', mesage=mesage)

@app.route("/search.html")
def search():
    return render_template("search.html")

@app.route("/submit_form", methods=["POST"])
def submit_form():
    selected_option = request.form.get('type')
    if selected_option == 'female':
        return redirect('/women.html')
    elif selected_option == 'transgender':
        return redirect('/trans.html')
    elif selected_option == 'Agriculture':
        return redirect('/farmer.html')
    elif selected_option == 'Students':
        return redirect('/student.html')
    else:
        return redirect('/')

@app.route("/women.html")
def woman():
    return render_template("women.html", headings=headings, dataW=dataW)

@app.route("/trans.html")
def trans():
    return render_template("trans.html", headings=headings, dataT=dataT)

@app.route("/farmer.html")
def farmer():
    return render_template("farmer.html", headings=headings, dataF=dataF)

@app.route("/student.html")
def student():
    return render_template("student.html", headings=headings, dataS=dataS)

@app.route("/catalogue.html")
def catalogue():
    return render_template('catalog.html')

@app.route("/woman1.html")
def woman1():
    return render_template('women1.html')

@app.route("/woman2.html")
def woman2():
    return render_template('women2.html')

@app.route("/woman3.html")
def woman3():
    return render_template('women3.html')

@app.route("/woman4.html")
def woman4():
    return render_template('women4.html')

@app.route("/woman5.html")
def woman5():
    return render_template('women5.html')

@app.route("/woman6.html")
def woman6():
    return render_template('women6.html')

@app.route("/woman7.html")
def woman7():
    return render_template('women7.html')

@app.route("/woman8.html")
def woman8():
    return render_template('women8.html')

@app.route("/woman9.html")
def woman9():
    return render_template('women9.html')

@app.route("/woman10.html")
def woman10():
    return render_template('women10.html')

@app.route("/trans1.html")
def trans1():
    return render_template('trans1.html')

@app.route("/trans2.html")
def trans2():
    return render_template('trans2.html')

@app.route("/trans3.html")
def trans3():
    return render_template('trans3.html')

@app.route("/trans4.html")
def trans4():
    return render_template('trans4.html')

@app.route("/trans5.html")
def trans5():
    return render_template('trans5.html')

@app.route("/trans6.html")
def trans6():
    return render_template('trans1.html')

@app.route("/trans7.html")
def trans7():
    return render_template('trans2.html')

@app.route("/trans8.html")
def trans8():
    return render_template('trans3.html')

@app.route("/trans9")
def trans9():
    return render_template('trans4.html')

@app.route("/trans10.html")
def trans10():
    return render_template('trans5.html')



@app.route("/student1.html")
def student1():
    return render_template('student1.html')

@app.route("/student2.html")
def student2():
    return render_template('student2.html')

@app.route("/student3.html")
def student3():
    return render_template('student3.html')

@app.route("/student4.html")
def student4():
    return render_template('student4.html')

@app.route("/student5.html")
def student5():
    return render_template('student5.html')

@app.route("/student6.html")
def student6():
    return render_template('student1.html')

@app.route("/student7.html")
def student7():
    return render_template('student2.html')

@app.route("/student8.html")
def student8():
    return render_template('student3.html')

@app.route("/student9")
def student9():
    return render_template('student4.html')

@app.route("/student10.html")
def student10():
    return render_template('student5.html')

@app.route("/farmer1.html")
def farmer1():
    return render_template('farmer1.html')

@app.route("/farmer2.html")
def farmer2():
    return render_template('farmer2.html')

@app.route("/farmer3.html")
def farmer3():
    return render_template('farmer3.html')

@app.route("/farmer4.html")
def farmer4():
    return render_template('farmer4.html')

@app.route("/farmer5.html")
def farmer5():
    return render_template('farmer5.html')

@app.route("/farmer6.html")
def farmer6():
    return render_template('farmer1.html')

@app.route("/farmer7.html")
def farmer7():
    return render_template('farmer2.html')

@app.route("/farmer8.html")
def farmer8():
    return render_template('farmer3.html')

@app.route("/farmer9")
def farmer9():
    return render_template('farmer4.html')

@app.route("/farmer10.html")
def farmer10():
    return render_template('farmer5.html')


if __name__ == '__main__':
    app.run(debug=True)
