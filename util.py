import random
import uuid


from constants import SERVICES_SOLUTIONS, FUNDING_AGENCIES

# Sample websites for generation
SAMPLE_DOMAINS = ["edu.in", "ac.in", "org.in", "res.in"]

# Sample institute types and domains
INSTITUTE_TYPES = ["Medical College", "Research Institute", "Government Hospital", "Private Hospital", "University Department"]
DOMAINS = [
    "Microbiology", "Genomics", "Proteomics", "Metabolomics",
    "Pharmacogenomics", "Oncology", "Public Health", "Molecular Biology"
]

CITIES = ["Patna"]

FIRST_NAMES = ["Priya", "Anjali", "Ravi", "Amit", "Sneha", "Arun", "Kiran", "Neha", "Deepak", "Manish"]
LAST_NAMES = ["Singh", "Sharma", "Kumar", "Yadav", "Sinha", "Jha", "Mishra", "Thakur", "Verma"]

DESIGNATIONS = [
    "Professor", "Associate Professor", "Assistant Professor",
    "Research Scientist", "Principal Investigator", "Lab Head"
]

def generate_institute():
    city = random.choice(CITIES)
    name = f"{random.choice(["AIIMS", "IGIMS", "NMCH", "PMCH", "Magadh University"])} {city}"
    inst_type = random.choice(INSTITUTE_TYPES)
    domain = random.sample(DOMAINS, k=random.randint(1, 3))
    website = f"https://www.{name.lower().replace(' ', '')}.{random.choice(SAMPLE_DOMAINS)}"
    return {
        "name": name,
        "location": city,
        "type": inst_type,
        "domain": domain,
        "website": website
    }

def generate_persons_for_institute(institute):
    domain = institute["domain"]
    website = institute["website"]
    email_domain = website.replace("https://", "").replace("http://", "").split("/")[0] or "example.edu.in"

    department_names = [f"{d} Department" for d in domain]
    people = []
    used_emails = set()

    for _ in range(random.randint(4, 6)):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        full_name = f"{fname} {lname}"
        designation = random.choice(DESIGNATIONS)
        expertise = random.choice(domain)
        department = f"{expertise} Department"

        base_email = f"{fname.lower()}.{lname.lower()}@{email_domain}"
        email = base_email
        suffix = 1
        while email in used_emails:
            email = f"{fname.lower()}.{lname.lower()}{suffix}@{email_domain}"
            suffix += 1
        used_emails.add(email)

        contact = f"+91-{random.randint(7000000000, 9999999999)}"
        linkedin = f"https://linkedin.com/in/{fname.lower()}-{lname.lower()}-{uuid.uuid4().hex[:4]}"

        person = {
            "person_name": full_name,
            "designation": designation,
            "email": email,
            "contact": contact,
            "linkedin": linkedin,
            "expertise": expertise,
            "department_name": department,
            "lab_name": f"{expertise} Research Lab"
        }
        people.append(person)
    return people

def match_services(domain_list):
    keywords = [d.lower() for d in domain_list]
    matched = [s for s in SERVICES_SOLUTIONS if any(k in s.lower() for k in keywords)]
    if not matched:
        matched = random.sample(SERVICES_SOLUTIONS, k=2)
    return matched

def assign_funding_agencies():
    return random.sample(FUNDING_AGENCIES, k=random.randint(2, 4))

def generate_data_for_state(state):
    rows = []
    for _ in range(random.randint(3, 5)):
        inst = generate_institute()
        people = generate_persons_for_institute(inst)
        services = match_services(inst["domain"])
        funders = assign_funding_agencies()

        for person in people:
            row = {
                "Institute Name": inst["name"],
                "Location": inst["location"],
                "Institute Website": inst["website"],
                "Department Name": person["department_name"],
                "Lab/Unit Name": person["lab_name"],
                "Person Name": person["person_name"],
                "Designation": person["designation"],
                "Email": person["email"],
                "Contact": person["contact"],
                "LinkedIn": person["linkedin"],
                "Primary Focus Area": person["expertise"],
                "Ongoing Projects": "Exploring advanced omics integration in patient diagnostics.",
                "Funding Agencies": ", ".join(funders),
                "Recent Publications": "https://pubmed.ncbi.nlm.nih.gov/PMID12345678/",
                "Services": ", ".join(services),
                "Matched Advait Solution(s)": ", ".join(services),
                "Match Category": "High Relevance"
            }
            rows.append(row)
    return rows
