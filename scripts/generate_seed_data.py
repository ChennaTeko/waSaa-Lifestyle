"""Generates the PROTOTYPE seed dataset. Run: python -m scripts.generate_seed_data

ALL providers below are FICTIONAL and ALL records are data_origin='synthetic'.
A few rows are DELIBERATELY DIRTY (messy spacing, wrong case, bad price/rating,
a duplicate) so the cleaning and validation stages have something real to do.
"""
import csv

from src.utils.config import RAW_DIR

COLS = ["provider_name", "service_name", "category", "description", "keywords", "area",
        "city", "price_min", "price_max", "rating_avg", "review_count",
        "availability_days", "data_origin"]

# provider, service, category, description, keywords, area, pmin, pmax, rating, reviews, availability
S = [
 # ---- Healthcare (bookable services only, no diagnosis) ----
 ("Westview Dental Clinic","Teeth cleaning and scaling","Healthcare","Professional dental cleaning and scaling by a qualified dentist to remove plaque and keep your gums healthy.","dentist, teeth, dental, scaling, oral hygiene","Westlands",3000,6000,4.6,120,"Mon-Sat"),
 ("Westview Dental Clinic","Teeth whitening","Healthcare","Safe in-clinic teeth whitening session for a brighter smile, done by a trained dental practitioner.","dentist, whitening, smile, dental","Westlands",8000,15000,4.6,120,"Mon-Sat"),
 ("Kilimani Physio Centre","Physiotherapy session","Healthcare","One-hour physiotherapy session for back pain recovery, sports injuries and mobility exercises with a registered physiotherapist.","physio, physiotherapist, back pain, sports injury, rehab","Kilimani",2500,4500,4.8,85,"Mon-Fri"),
 ("Kilimani Physio Centre","Home physiotherapy visit","Healthcare","A physiotherapist visits your home for rehabilitation exercises, ideal for elderly patients and post-surgery recovery.","home visit, physio, elderly, rehabilitation","Kilimani",4000,7000,4.8,85,"Mon-Fri"),
 ("Lavington Eye Care","Eye test and glasses fitting","Healthcare","Comprehensive eye examination followed by prescription glasses fitting with a wide range of frames.","optician, eye test, glasses, spectacles","Lavington",1500,3500,4.4,60,"Mon-Sat"),
 ("CityCare Lab Services","Home blood test collection","Healthcare","A phlebotomist collects your blood sample at home and results are sent to you by email within a day.","lab, blood test, home collection, phlebotomist","CBD",1200,4000,4.3,210,"Daily"),
 ("Karen Family Clinic","General consultation booking","Healthcare","Book a routine appointment with a general practitioner at our family clinic for check ups and vaccinations.","doctor, clinic, appointment, checkup, vaccination","Karen",2000,3500,4.5,95,"Mon-Sun"),
 ("Parklands Mind Wellness","Counselling session","Healthcare","Confidential one-on-one counselling session with a licensed counsellor for stress, relationships and life changes.","counsellor, therapy, mental health, stress","Parklands",3000,5000,4.7,70,"Mon-Sat"),
 # ---- Transport ----
 ("SafeRide Airport Transfers","Airport pickup and drop-off","Transport","Reliable private car transfer to and from Jomo Kenyatta airport with flight tracking and a professional driver.","airport, taxi, pickup, JKIA, transfer","Embakasi",2000,3500,4.7,300,"Daily"),
 ("MoveFast Movers","House moving service","Transport","Full house moving with a truck, loaders and careful packing of furniture across Nairobi and its environs.","movers, relocation, truck, furniture, moving","South B",8000,30000,4.2,140,"Mon-Sun"),
 ("Kasarani Boda Express","Motorbike delivery within Nairobi","Transport","Fast motorbike courier for parcels and documents delivered the same day anywhere in the city.","boda, courier, delivery, parcel, motorbike","Kasarani",300,1200,4.0,420,"Daily"),
 ("Ruaka School Shuttles","School and office shuttle","Transport","Monthly shuttle service picking up children or staff from home each morning and returning them in the evening.","shuttle, school bus, commute, monthly","Ruaka",6000,15000,4.5,55,"Mon-Fri"),
 ("Executive Cars Nairobi","Chauffeur car hire","Transport","Hire a clean sedan with a chauffeur by the hour or the day for meetings, weddings and corporate events.","car hire, chauffeur, wedding car, driver","Westlands",5000,20000,4.6,90,"Daily"),
 ("Rongai Pickup Hauling","Pickup truck hauling","Transport","Small pickup truck for hauling building materials, furniture and bulky items over short distances.","pickup, hauling, transport goods, lorry","Rongai",2500,8000,4.1,40,"Mon-Sat"),
 ("CBD Cab Connect","Late night taxi","Transport","Safe late night taxi rides across Nairobi with verified drivers and fixed prices agreed before the trip.","taxi, night, cab, safe ride","CBD",500,3000,4.3,260,"Daily"),
 ("Lavington Car Wash Mobile","Mobile car wash","Transport","We come to your home or office and wash and vacuum your car using water saving equipment.","car wash, detailing, mobile, vehicle cleaning","Lavington",800,2500,4.4,110,"Daily"),
 # ---- Beauty & Wellness ----
 ("Glow Salon Westlands","Box braids","Beauty & Wellness","Neat box braids in different sizes and lengths done by experienced braiders using quality hair extensions.","braids, hair, plaiting, salon, hairdresser","Westlands",3500,8000,4.7,200,"Mon-Sun"),
 ("Glow Salon Westlands","Bridal makeup","Beauty & Wellness","Complete bridal makeup with trial session and touch up kit for your wedding day, done by a professional artist.","makeup, bride, wedding, makeup artist","Westlands",8000,25000,4.7,200,"Mon-Sun"),
 ("Kilimani Nails Studio","Gel manicure and pedicure","Beauty & Wellness","Long lasting gel manicure and relaxing pedicure by a skilled nail technician in a clean quiet studio.","nails, manicure, pedicure, nail technician, gel","Kilimani",2000,4500,4.5,150,"Mon-Sat"),
 ("Karen Spa Retreat","Deep tissue massage","Beauty & Wellness","Sixty minute deep tissue massage to relieve muscle tension and stress in a calm spa setting.","massage, spa, relaxation, muscle pain","Karen",4000,8000,4.8,180,"Mon-Sun"),
 ("Sharp Cuts Barbershop","Mens haircut and beard trim","Beauty & Wellness","Precision mens haircut with beard shaping and a hot towel finish at an affordable barbershop price.","barber, haircut, beard, shave, kinyozi","Kasarani",300,800,4.3,330,"Daily"),
 ("Kileleshwa Fit Hub","Personal training session","Beauty & Wellness","One on one personal training for weight loss, strength and fitness goals with a certified trainer.","gym, trainer, fitness, weight loss, workout","Kileleshwa",2000,4000,4.6,75,"Mon-Sat"),
 ("Lavington Yoga Space","Group yoga class","Beauty & Wellness","Beginner friendly group yoga classes focusing on flexibility, breathing and stress relief.","yoga, stretching, wellness, class, meditation","Lavington",1000,1800,4.6,65,"Mon-Fri"),
 ("Parklands Lash Bar","Eyelash extensions","Beauty & Wellness","Natural looking classic and volume eyelash extensions applied by a trained lash technician.","lashes, eyelash, beauty, extensions","Parklands",2500,5500,4.4,90,"Mon-Sat"),
 # ---- Domestic Services ----
 ("Sparkle Home Cleaners","Deep house cleaning","Domestic Services","Thorough deep cleaning of your house including kitchen, bathrooms, floors and windows by a trained team.","cleaning, cleaners, house cleaning, deep clean","Kilimani",3000,9000,4.5,230,"Mon-Sun"),
 ("Sparkle Home Cleaners","Sofa and carpet cleaning","Domestic Services","Professional shampooing and steam cleaning of sofas and carpets that removes stains and bad smells.","carpet, sofa, upholstery, steam cleaning","Kilimani",2500,7000,4.5,230,"Mon-Sun"),
 ("QuickFix Plumbers","Emergency plumbing repair","Domestic Services","Fast response plumber for leaking pipes, blocked sinks, toilets and water heater problems at any hour.","plumber, leak, pipes, blocked drain, water","Karen",1500,6000,4.2,175,"Daily"),
 ("BrightSpark Electricians","Electrical wiring and repair","Domestic Services","Licensed electrician for house wiring, socket and light installation, and fixing power faults safely.","electrician, wiring, power, lights, sockets","Kileleshwa",1500,7000,4.4,160,"Mon-Sat"),
 ("Green Thumb Gardeners","Garden maintenance","Domestic Services","Regular lawn mowing, hedge trimming and flower bed care to keep your compound neat and green.","gardener, lawn, hedge, landscaping, compound","Karen",2000,6000,4.3,80,"Mon-Sat"),
 ("TrustedHelp Nannies","Nanny placement","Domestic Services","Vetted and experienced nannies and house helps matched to your family with references checked.","nanny, house help, maid, childcare, domestic worker","Westlands",5000,12000,4.5,100,"Mon-Fri"),
 ("PestAway Nairobi","Pest control and fumigation","Domestic Services","Safe fumigation to get rid of cockroaches, bed bugs, rats and ants in homes and offices.","pest, fumigation, cockroaches, bed bugs, rats","South B",3000,10000,4.2,120,"Mon-Sat"),
 ("Embakasi Fundi Works","Furniture and carpentry repair","Domestic Services","Skilled carpenter for repairing doors, wardrobes and tables and making custom furniture to order.","carpenter, fundi, furniture, repair, woodwork","Embakasi",1500,8000,4.1,60,"Mon-Sat"),
 # ---- Education Support ----
 ("BrainBoost Tutors","Maths home tutoring","Education Support","Private home tutoring in mathematics for primary and high school students by a trained teacher.","maths, tutor, tuition, home tutor, mathematics","Lavington",1200,2500,4.7,90,"Mon-Sat"),
 ("BrainBoost Tutors","KCSE revision classes","Education Support","Intensive revision classes for KCSE candidates covering past papers, exam technique and difficult topics.","KCSE, revision, exams, form four, past papers","Lavington",800,2000,4.7,90,"Mon-Sat"),
 ("Kileleshwa Music Academy","Piano lessons","Education Support","Weekly piano lessons for children and adults, from complete beginners to grade exam preparation.","piano, music lessons, instrument, keyboard","Kileleshwa",1500,3000,4.6,45,"Mon-Sat"),
 ("CodeKids Nairobi","Kids coding classes","Education Support","Fun weekend coding classes where children aged eight to fifteen learn Scratch and Python.","coding, programming, kids, computer, python","Parklands",2000,4000,4.8,55,"Sat-Sun"),
 ("SpeakWell Language Hub","English and French lessons","Education Support","Small group and one on one language lessons to improve speaking, writing and exam performance.","language, english, french, lessons, speaking","CBD",1500,3500,4.3,70,"Mon-Sat"),
 ("Ruaka Homework Club","After school homework help","Education Support","Supervised after school homework support and reading practice for primary school pupils.","homework, after school, primary, supervision","Ruaka",500,1500,4.4,50,"Mon-Fri"),
 ("DriveSure Driving School","Driving lessons","Education Support","Learn to drive with a patient instructor and prepare for the NTSA driving test in a dual control car.","driving school, driving lessons, NTSA, instructor, learner","South B",8000,18000,4.4,130,"Mon-Sat"),
 ("CareerEdge Coaching","CV writing and interview coaching","Education Support","Get your CV polished and practise interviews with a career coach to land your next job.","CV, resume, interview, career, coaching","Westlands",2000,5000,4.5,40,"Mon-Fri"),
]

# deliberately dirty rows (for demonstrating cleaning/validation)
DIRTY = [
 ["  Glow   Salon Westlands ","Hair  Relaxer","beauty","Professional hair relaxing treatment with conditioning for smooth manageable hair at the salon.","hair, relaxer ,salon","westlands",2500,5000,4.5,200,"Mon-Sun","SYNTHETIC"],       # fixable
 ["Mombasa Road Tyres","Wheel alignment","Transport","Tyres.","tyres","Embakasi",1000,2000,4.0,20,"Mon-Sat","synthetic"],                                                                              # short desc -> reject
 ["QuickFix Plumbers","Water tank cleaning","Domestic Services","Cleaning and disinfecting of household water tanks to keep your drinking water safe and clean.","tank, water, cleaning","Karen",5000,2000,4.2,175,"Mon-Sat","synthetic"], # price min>max -> reject
 ["Westview Dental Clinic","Teeth cleaning and scaling","Healthcare","Professional dental cleaning and scaling by a qualified dentist to remove plaque and keep your gums healthy.","dentist","Westlands",3000,6000,4.6,120,"Mon-Sat","synthetic"],  # duplicate -> reject
 ["Impossible Rating Cafe","Barista training","Education Support","Hands on barista training course covering espresso, milk texturing and cafe customer service skills.","barista, coffee","CBD",3000,6000,7.2,10,"Mon-Fri","synthetic"],  # rating 7.2 -> reject
 ["Fantasy Land Tours","Space tourism","Transport","A pretend service in a place that does not exist used to test the area validation rule properly.","space","Atlantis",1000,2000,4.0,1,"Daily","synthetic"],                       # unknown area -> reject
 ["Free Quote Painters","House painting","Domestic Services","Interior and exterior house painting with quality paint and a neat finish by an experienced painting crew.","painter, painting","Kasarani","","",4.0,30,"Mon-Sat","synthetic"],  # missing price -> allowed (NULL)
]

QUERIES = [
 # query_text, query_type, target_category, location_constraint, budget_max
 ("I need an affordable saloonist near Westlands","typo","Beauty & Wellness","Westlands",""),
 ("find me someone to braid my hair this weekend","synonym","Beauty & Wellness","",""),
 ("cheap haircut in Kasarani","price-aware","Beauty & Wellness","Kasarani",1000),
 ("bridal makeup artist","clear","Beauty & Wellness","",""),
 ("I want to relax after a stressful week","vague","Beauty & Wellness","",""),
 ("dentist for teeth cleaning","clear","Healthcare","",""),
 ("someone to treat my back pain at home","vague","Healthcare","",""),
 ("physio in Kilimani under 5000","price-aware","Healthcare","Kilimani",5000),
 ("I feel anxious and need someone to talk to","vague","Healthcare","",""),
 ("get my eyes checked and buy glasses","multi-intent","Healthcare","",""),
 ("taxi to the airport early morning","clear","Transport","",""),
 ("I am moving house next month and need a truck and people to carry things","multi-intent","Transport","",""),
 ("send a parcel across town today","synonym","Transport","",""),
 ("someone to wash my car at home","clear","Transport","",""),
 ("find me a reliable electrician who can come to Karen","clear","Domestic Services","Karen",""),
 ("my sink is blocked and water is leaking","vague","Domestic Services","",""),
 ("house help for my kids","synonym","Domestic Services","",""),
 ("clean my sofas and carpets","clear","Domestic Services","",""),
 ("cockroaches everywhere in my flat","vague","Domestic Services","",""),
 ("maths tutor for my son in form three","clear","Education Support","",""),
 ("where can my child learn to code","vague","Education Support","",""),
 ("learn to play an instrument","vague","Education Support","",""),
 ("I want to get my driving licence","vague","Education Support","",""),
 ("help me improve my CV and prepare for job interviews","multi-intent","Education Support","",""),
]


def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_DIR / "services_raw.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(COLS)
        for p, sv, cat, d, kw, area, a, b, r, n, av in S:
            w.writerow([p, sv, cat, d, kw, area, "Nairobi", a, b, r, n, av, "synthetic"])
        for p, sv, cat, d, kw, area, a, b, r, n, av, origin in DIRTY:
            w.writerow([p, sv, cat, d, kw, area, "Nairobi", a, b, r, n, av, origin])
    with open(RAW_DIR / "queries_seed.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["query_text", "query_type", "target_category", "location_constraint",
                    "budget_max", "language", "created_by"])
        for q in QUERIES:
            w.writerow([*q, "en", "manual"])
    print(f"Wrote {len(S) + len(DIRTY)} service rows and {len(QUERIES)} queries to {RAW_DIR}")


if __name__ == "__main__":
    main()
