"""Seed comprehensive Indian courts database."""
from __future__ import annotations
import psycopg

DB_URL = "postgresql://postgres.ksbjxfvxzccibrzhizfv:Advox%402026%402025@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres"

SUPREME_COURT = {
    "name": "Supreme Court of India",
    "short_name": "SCI",
    "court_type": "supreme_court",
    "state_code": "DL",
    "state_name": "Delhi",
    "ecourt_code": "SCI",
    "bench": "Principal",
    "address": "Tilak Marg, New Delhi - 110001",
    "website": "https://main.sci.gov.in",
}

HIGH_COURTS = [
    {"name": "Allahabad High Court", "short_name": "AHC", "state_code": "UP", "state_name": "Uttar Pradesh", "ecourt_code": "allahabad", "bench": "Allahabad, Lucknow", "website": "https://www.allahabadhighcourt.in"},
    {"name": "Andhra Pradesh High Court", "short_name": "APHC", "state_code": "AP", "state_name": "Andhra Pradesh", "ecourt_code": "aphc", "bench": "Amaravati", "website": "https://aphc.gov.in"},
    {"name": "Bombay High Court", "short_name": "BHC", "state_code": "MH", "state_name": "Maharashtra", "ecourt_code": "bombay", "bench": "Mumbai, Nagpur, Aurangabad, Goa", "website": "https://bombayhighcourt.nic.in"},
    {"name": "Calcutta High Court", "short_name": "CHC", "state_code": "WB", "state_name": "West Bengal", "ecourt_code": "calcutta", "bench": "Calcutta, Port Blair", "website": "https://www.calcuttahighcourt.gov.in"},
    {"name": "Chhattisgarh High Court", "short_name": "CGHC", "state_code": "CG", "state_name": "Chhattisgarh", "ecourt_code": "cghc", "bench": "Bilaspur", "website": "https://highcourt.cg.gov.in"},
    {"name": "Delhi High Court", "short_name": "DHC", "state_code": "DL", "state_name": "Delhi", "ecourt_code": "delhi", "bench": "New Delhi", "website": "https://delhihighcourt.nic.in"},
    {"name": "Gauhati High Court", "short_name": "GHC", "state_code": "AS", "state_name": "Assam", "ecourt_code": "gauhati", "bench": "Guwahati, Kohima, Aizawl, Itanagar", "website": "https://ghconline.gov.in"},
    {"name": "Gujarat High Court", "short_name": "GJHC", "state_code": "GJ", "state_name": "Gujarat", "ecourt_code": "gujarat", "bench": "Ahmedabad", "website": "https://gujarathighcourt.nic.in"},
    {"name": "Himachal Pradesh High Court", "short_name": "HPHC", "state_code": "HP", "state_name": "Himachal Pradesh", "ecourt_code": "hphc", "bench": "Shimla", "website": "https://hphighcourt.nic.in"},
    {"name": "Jammu & Kashmir and Ladakh High Court", "short_name": "JKHC", "state_code": "JK", "state_name": "Jammu & Kashmir", "ecourt_code": "jkhc", "bench": "Srinagar, Jammu", "website": "https://jkhighcourt.nic.in"},
    {"name": "Jharkhand High Court", "short_name": "JHHC", "state_code": "JH", "state_name": "Jharkhand", "ecourt_code": "jharkhand", "bench": "Ranchi", "website": "https://jharkhandhighcourt.nic.in"},
    {"name": "Karnataka High Court", "short_name": "KHC", "state_code": "KA", "state_name": "Karnataka", "ecourt_code": "karnataka", "bench": "Bengaluru, Dharwad, Kalaburagi", "website": "https://karnatakajudiciary.kar.nic.in"},
    {"name": "Kerala High Court", "short_name": "KLHC", "state_code": "KL", "state_name": "Kerala", "ecourt_code": "kerala", "bench": "Ernakulam", "website": "https://highcourtofkerala.nic.in"},
    {"name": "Madhya Pradesh High Court", "short_name": "MPHC", "state_code": "MP", "state_name": "Madhya Pradesh", "ecourt_code": "mphc", "bench": "Jabalpur, Indore, Gwalior", "website": "https://mphc.gov.in"},
    {"name": "Madras High Court", "short_name": "MHC", "state_code": "TN", "state_name": "Tamil Nadu", "ecourt_code": "madras", "bench": "Chennai, Madurai", "website": "https://www.mhc.tn.gov.in"},
    {"name": "Manipur High Court", "short_name": "MNHC", "state_code": "MN", "state_name": "Manipur", "ecourt_code": "manipur", "bench": "Imphal", "website": "https://hcmimphal.nic.in"},
    {"name": "Meghalaya High Court", "short_name": "MLHC", "state_code": "ML", "state_name": "Meghalaya", "ecourt_code": "meghalaya", "bench": "Shillong", "website": "https://meghalayahighcourt.nic.in"},
    {"name": "Orissa High Court", "short_name": "OHC", "state_code": "OD", "state_name": "Odisha", "ecourt_code": "orissa", "bench": "Cuttack", "website": "https://orissahighcourt.nic.in"},
    {"name": "Patna High Court", "short_name": "PHC", "state_code": "BR", "state_name": "Bihar", "ecourt_code": "patna", "bench": "Patna", "website": "https://patnahighcourt.gov.in"},
    {"name": "Punjab and Haryana High Court", "short_name": "PHHC", "state_code": "PB", "state_name": "Punjab", "ecourt_code": "phhc", "bench": "Chandigarh", "website": "https://phhc.gov.in"},
    {"name": "Rajasthan High Court", "short_name": "RHC", "state_code": "RJ", "state_name": "Rajasthan", "ecourt_code": "rajasthan", "bench": "Jodhpur, Jaipur", "website": "https://hcraj.nic.in"},
    {"name": "Sikkim High Court", "short_name": "SKHC", "state_code": "SK", "state_name": "Sikkim", "ecourt_code": "sikkim", "bench": "Gangtok", "website": "https://hcsikkim.gov.in"},
    {"name": "Telangana High Court", "short_name": "TSHC", "state_code": "TS", "state_name": "Telangana", "ecourt_code": "tshc", "bench": "Hyderabad", "website": "https://tshc.gov.in"},
    {"name": "Tripura High Court", "short_name": "TRHC", "state_code": "TR", "state_name": "Tripura", "ecourt_code": "tripura", "bench": "Agartala", "website": "https://thc.nic.in"},
    {"name": "Uttarakhand High Court", "short_name": "UKHC", "state_code": "UK", "state_name": "Uttarakhand", "ecourt_code": "uttarakhand", "bench": "Nainital", "website": "https://highcourtofuttarakhand.gov.in"},
]

# West Bengal district courts — all 23 districts
WB_DISTRICT_COURTS = [
    {"district": "Alipurduar", "ecourt_district_code": "1"},
    {"district": "Bankura", "ecourt_district_code": "2"},
    {"district": "Birbhum", "ecourt_district_code": "3"},
    {"district": "Cooch Behar", "ecourt_district_code": "4"},
    {"district": "Dakshin Dinajpur", "ecourt_district_code": "5"},
    {"district": "Darjeeling", "ecourt_district_code": "6"},
    {"district": "Hooghly", "ecourt_district_code": "7"},
    {"district": "Howrah", "ecourt_district_code": "8"},
    {"district": "Jalpaiguri", "ecourt_district_code": "9"},
    {"district": "Jhargram", "ecourt_district_code": "10"},
    {"district": "Kalimpong", "ecourt_district_code": "11"},
    {"district": "Kolkata", "ecourt_district_code": "12"},
    {"district": "Malda", "ecourt_district_code": "13"},
    {"district": "Murshidabad", "ecourt_district_code": "14"},
    {"district": "Nadia", "ecourt_district_code": "15"},
    {"district": "North 24 Parganas", "ecourt_district_code": "16"},
    {"district": "Paschim Bardhaman", "ecourt_district_code": "17"},
    {"district": "Paschim Medinipur", "ecourt_district_code": "18"},
    {"district": "Purba Bardhaman", "ecourt_district_code": "19"},
    {"district": "Purba Medinipur", "ecourt_district_code": "20"},
    {"district": "Purulia", "ecourt_district_code": "21"},
    {"district": "South 24 Parganas", "ecourt_district_code": "22"},
    {"district": "Uttar Dinajpur", "ecourt_district_code": "23"},
]

# Pan-India key district courts (major cities from each state)
MAJOR_DISTRICT_COURTS = [
    # Maharashtra
    {"district": "Mumbai City", "state_code": "MH", "state_name": "Maharashtra", "ecourt_state_code": "10"},
    {"district": "Mumbai Suburban", "state_code": "MH", "state_name": "Maharashtra", "ecourt_state_code": "10"},
    {"district": "Pune", "state_code": "MH", "state_name": "Maharashtra", "ecourt_state_code": "10"},
    {"district": "Nagpur", "state_code": "MH", "state_name": "Maharashtra", "ecourt_state_code": "10"},
    {"district": "Thane", "state_code": "MH", "state_name": "Maharashtra", "ecourt_state_code": "10"},
    # Delhi
    {"district": "Central Delhi", "state_code": "DL", "state_name": "Delhi", "ecourt_state_code": "6"},
    {"district": "New Delhi", "state_code": "DL", "state_name": "Delhi", "ecourt_state_code": "6"},
    {"district": "North Delhi", "state_code": "DL", "state_name": "Delhi", "ecourt_state_code": "6"},
    {"district": "South Delhi", "state_code": "DL", "state_name": "Delhi", "ecourt_state_code": "6"},
    {"district": "East Delhi", "state_code": "DL", "state_name": "Delhi", "ecourt_state_code": "6"},
    {"district": "West Delhi", "state_code": "DL", "state_name": "Delhi", "ecourt_state_code": "6"},
    # Karnataka
    {"district": "Bengaluru Urban", "state_code": "KA", "state_name": "Karnataka", "ecourt_state_code": "3"},
    {"district": "Mysuru", "state_code": "KA", "state_name": "Karnataka", "ecourt_state_code": "3"},
    # Tamil Nadu
    {"district": "Chennai", "state_code": "TN", "state_name": "Tamil Nadu", "ecourt_state_code": "25"},
    {"district": "Coimbatore", "state_code": "TN", "state_name": "Tamil Nadu", "ecourt_state_code": "25"},
    {"district": "Madurai", "state_code": "TN", "state_name": "Tamil Nadu", "ecourt_state_code": "25"},
    # Uttar Pradesh
    {"district": "Lucknow", "state_code": "UP", "state_name": "Uttar Pradesh", "ecourt_state_code": "26"},
    {"district": "Varanasi", "state_code": "UP", "state_name": "Uttar Pradesh", "ecourt_state_code": "26"},
    {"district": "Allahabad (Prayagraj)", "state_code": "UP", "state_name": "Uttar Pradesh", "ecourt_state_code": "26"},
    {"district": "Agra", "state_code": "UP", "state_name": "Uttar Pradesh", "ecourt_state_code": "26"},
    # Gujarat
    {"district": "Ahmedabad", "state_code": "GJ", "state_name": "Gujarat", "ecourt_state_code": "24"},
    {"district": "Surat", "state_code": "GJ", "state_name": "Gujarat", "ecourt_state_code": "24"},
    {"district": "Vadodara", "state_code": "GJ", "state_name": "Gujarat", "ecourt_state_code": "24"},
    # Rajasthan
    {"district": "Jaipur", "state_code": "RJ", "state_name": "Rajasthan", "ecourt_state_code": "20"},
    {"district": "Jodhpur", "state_code": "RJ", "state_name": "Rajasthan", "ecourt_state_code": "20"},
    # Kerala
    {"district": "Ernakulam", "state_code": "KL", "state_name": "Kerala", "ecourt_state_code": "21"},
    {"district": "Thiruvananthapuram", "state_code": "KL", "state_name": "Kerala", "ecourt_state_code": "21"},
    # Telangana
    {"district": "Hyderabad", "state_code": "TS", "state_name": "Telangana", "ecourt_state_code": "28"},
    {"district": "Rangareddy", "state_code": "TS", "state_name": "Telangana", "ecourt_state_code": "28"},
    # Andhra Pradesh
    {"district": "Visakhapatnam", "state_code": "AP", "state_name": "Andhra Pradesh", "ecourt_state_code": "1"},
    {"district": "Guntur", "state_code": "AP", "state_name": "Andhra Pradesh", "ecourt_state_code": "1"},
    # Bihar
    {"district": "Patna", "state_code": "BR", "state_name": "Bihar", "ecourt_state_code": "4"},
    # Odisha
    {"district": "Cuttack", "state_code": "OD", "state_name": "Odisha", "ecourt_state_code": "18"},
    {"district": "Bhubaneswar (Khordha)", "state_code": "OD", "state_name": "Odisha", "ecourt_state_code": "18"},
    # Assam
    {"district": "Kamrup Metropolitan", "state_code": "AS", "state_name": "Assam", "ecourt_state_code": "2"},
    # Punjab
    {"district": "Ludhiana", "state_code": "PB", "state_name": "Punjab", "ecourt_state_code": "19"},
    {"district": "Amritsar", "state_code": "PB", "state_name": "Punjab", "ecourt_state_code": "19"},
    # Haryana
    {"district": "Gurugram", "state_code": "HR", "state_name": "Haryana", "ecourt_state_code": "7"},
    {"district": "Faridabad", "state_code": "HR", "state_name": "Haryana", "ecourt_state_code": "7"},
    # Madhya Pradesh
    {"district": "Bhopal", "state_code": "MP", "state_name": "Madhya Pradesh", "ecourt_state_code": "11"},
    {"district": "Indore", "state_code": "MP", "state_name": "Madhya Pradesh", "ecourt_state_code": "11"},
    # Chhattisgarh
    {"district": "Raipur", "state_code": "CG", "state_name": "Chhattisgarh", "ecourt_state_code": "33"},
    # Jharkhand
    {"district": "Ranchi", "state_code": "JH", "state_name": "Jharkhand", "ecourt_state_code": "34"},
    # Uttarakhand
    {"district": "Dehradun", "state_code": "UK", "state_name": "Uttarakhand", "ecourt_state_code": "29"},
    # Goa
    {"district": "North Goa", "state_code": "GA", "state_name": "Goa", "ecourt_state_code": "30"},
    {"district": "South Goa", "state_code": "GA", "state_name": "Goa", "ecourt_state_code": "30"},
]


def seed():
    conn = psycopg.connect(DB_URL)
    cur = conn.cursor()

    # Clear existing
    cur.execute("DELETE FROM courts")

    # Supreme Court
    cur.execute(
        "INSERT INTO courts (name, short_name, court_type, state_code, state_name, ecourt_code, bench, address, website) "
        "VALUES (%(name)s, %(short_name)s, 'supreme_court', %(state_code)s, %(state_name)s, %(ecourt_code)s, %(bench)s, %(address)s, %(website)s) "
        "RETURNING id",
        SUPREME_COURT,
    )
    sci_id = cur.fetchone()[0]
    print(f"Supreme Court: {sci_id}")

    # High Courts
    hc_ids = {}
    for hc in HIGH_COURTS:
        cur.execute(
            "INSERT INTO courts (name, short_name, court_type, state_code, state_name, ecourt_code, bench, website, parent_court_id) "
            "VALUES (%s, %s, 'high_court', %s, %s, %s, %s, %s, %s) "
            "RETURNING id",
            (hc["name"], hc["short_name"], hc["state_code"], hc["state_name"], hc["ecourt_code"], hc["bench"], hc["website"], sci_id),
        )
        hc_id = cur.fetchone()[0]
        hc_ids[hc["state_code"]] = hc_id

    print(f"High Courts: {len(hc_ids)}")

    # WB District Courts
    wb_hc_id = hc_ids.get("WB")
    wb_count = 0
    for dc in WB_DISTRICT_COURTS:
        cur.execute(
            "INSERT INTO courts (name, short_name, court_type, state_code, state_name, district_name, ecourt_state_code, ecourt_district_code, parent_court_id) "
            "VALUES (%s, %s, 'district_court', 'WB', 'West Bengal', %s, '31', %s, %s)",
            (
                f"District & Sessions Court, {dc['district']}",
                f"DC-{dc['district'][:3].upper()}",
                dc["district"],
                dc["ecourt_district_code"],
                wb_hc_id,
            ),
        )
        wb_count += 1
    print(f"WB District Courts: {wb_count}")

    # Major district courts pan-India
    major_count = 0
    for dc in MAJOR_DISTRICT_COURTS:
        parent_hc_id = hc_ids.get(dc["state_code"])
        cur.execute(
            "INSERT INTO courts (name, short_name, court_type, state_code, state_name, district_name, ecourt_state_code, parent_court_id) "
            "VALUES (%s, %s, 'district_court', %s, %s, %s, %s, %s)",
            (
                f"District & Sessions Court, {dc['district']}",
                f"DC-{dc['district'][:3].upper()}",
                dc["state_code"],
                dc["state_name"],
                dc["district"],
                dc.get("ecourt_state_code", ""),
                parent_hc_id,
            ),
        )
        major_count += 1
    print(f"Major District Courts: {major_count}")

    conn.commit()
    print(f"\nTotal: 1 SC + {len(hc_ids)} HCs + {wb_count} WB DCs + {major_count} major DCs = {1 + len(hc_ids) + wb_count + major_count}")
    conn.close()


if __name__ == "__main__":
    seed()
