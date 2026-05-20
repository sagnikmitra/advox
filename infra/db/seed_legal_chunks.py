"""
Seed legal_source_chunks with substantive Indian legal content.

Covers: BNS/IPC criminal provisions, BNSS/CrPC procedures, BSA evidence,
Constitution fundamental rights, and common legal procedures (FIR, bail,
anticipatory bail, etc.)

Run: python3 infra/db/seed_legal_chunks.py
"""
from __future__ import annotations

import os
import psycopg
from psycopg.rows import dict_row

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres.ksbjxfvxzccibrzhizfv:Advox%402026%402025@aws-1-ap-northeast-1.pooler.supabase.com:6543/postgres",
)

# ---------------------------------------------------------------------------
# Legal content corpus — each entry maps to a source + chunk(s)
# ---------------------------------------------------------------------------

SOURCES = [
    # --- BNS (Bharatiya Nyaya Sanhita, 2023) — replaces IPC ---
    {
        "title": "Bharatiya Nyaya Sanhita, 2023 (BNS)",
        "source_type": "statute",
        "authority_level": "central_statute",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/19807",
        "source_domain": "indiacode.nic.in",
        "act_name": "Bharatiya Nyaya Sanhita, 2023",
        "language": "en",
        "chunks": [
            {
                "section": "1",
                "text": (
                    "BNS Section 1 — Short title, commencement and application. "
                    "(1) This Sanhita may be called the Bharatiya Nyaya Sanhita, 2023. "
                    "(2) It shall come into force on such date as the Central Government may, by notification in the Official Gazette, appoint. "
                    "(3) Every person shall be liable to punishment under this Sanhita and not otherwise for every act or omission contrary to the provisions thereof, of which he shall be guilty within India. "
                    "The BNS replaces the Indian Penal Code, 1860 (IPC) effective 1 July 2024."
                ),
            },
            {
                "section": "63",
                "text": (
                    "BNS Section 63 — Rape. A man is said to commit rape if he performs any of the acts specified under this section against a woman under the circumstances listed. "
                    "This section corresponds to the erstwhile IPC Section 375. "
                    "Punishment: Rigorous imprisonment for not less than ten years, which may extend to imprisonment for life, and shall also be liable to fine. "
                    "The definition covers penetration, manipulation of body, and application of mouth. Consent obtained by fear, intoxication, unsoundness of mind, or impersonation is not valid consent."
                ),
            },
            {
                "section": "64",
                "text": (
                    "BNS Section 64 — Punishment for rape. Whoever commits rape shall be punished with rigorous imprisonment of either description for a term which shall not be less than ten years, "
                    "but which may extend to imprisonment for life, and shall also be liable to fine. "
                    "Corresponds to erstwhile IPC Section 376."
                ),
            },
            {
                "section": "100",
                "text": (
                    "BNS Section 100 — Murder. Except in the cases hereinafter excepted, culpable homicide is murder, "
                    "if the act by which the death is caused is done with the intention of causing death, or if the act is done with the intention of causing such bodily injury as the offender knows to be likely to cause the death, "
                    "or if the act is done with the intention of causing bodily injury to any person and the bodily injury intended to be inflicted is sufficient in the ordinary course of nature to cause death, "
                    "or if the person committing the act knows that it is so imminently dangerous that it must, in all probability, cause death. "
                    "Corresponds to erstwhile IPC Section 300. Punishment under BNS Section 101: death or imprisonment for life, and fine."
                ),
            },
            {
                "section": "101",
                "text": (
                    "BNS Section 101 — Punishment for murder. Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine. "
                    "Corresponds to erstwhile IPC Section 302."
                ),
            },
            {
                "section": "109",
                "text": (
                    "BNS Section 109 — Attempt to murder. Whoever does any act with such intention or knowledge, and under such circumstances that, if he by that act caused death, "
                    "he would be guilty of murder, shall be punished with imprisonment of either description for a term which may extend to ten years, and shall also be liable to fine; "
                    "and if hurt is caused to any person by such act, the offender shall be liable either to imprisonment for life, or to such punishment as is hereinbefore mentioned. "
                    "Corresponds to erstwhile IPC Section 307."
                ),
            },
            {
                "section": "303",
                "text": (
                    "BNS Section 303 — Theft. Whoever, intending to take dishonestly any moveable property out of the possession of any person without that person's consent, "
                    "moves that property in order to such taking, is said to commit theft. Punishment: imprisonment up to three years, or fine, or both. "
                    "Corresponds to erstwhile IPC Section 378-379."
                ),
            },
            {
                "section": "308",
                "text": (
                    "BNS Section 308 — Extortion. Whoever intentionally puts any person in fear of any injury to that person, or to any other, "
                    "and thereby dishonestly induces the person so put in fear to deliver to any person any property, or valuable security, "
                    "or anything signed or sealed which may be converted into a valuable security, commits extortion. "
                    "Punishment: imprisonment up to three years, or fine, or both. Corresponds to erstwhile IPC Section 383-384."
                ),
            },
            {
                "section": "318",
                "text": (
                    "BNS Section 318 — Cheating. Whoever, by deceiving any person, fraudulently or dishonestly induces the person so deceived to deliver any property to any person, "
                    "or to consent that any person shall retain any property, or intentionally induces the person so deceived to do or omit to do anything which he would not do or omit if he were not so deceived, "
                    "and which act or omission causes or is likely to cause damage or harm to that person in body, mind, reputation or property, is said to cheat. "
                    "Punishment: imprisonment up to three years, or fine, or both. Corresponds to erstwhile IPC Section 415-417."
                ),
            },
            {
                "section": "351",
                "text": (
                    "BNS Section 351 — Criminal intimidation. Whoever threatens another with any injury to his person, reputation or property, "
                    "or to the person or reputation of any one in whom that person is interested, with intent to cause alarm to that person, "
                    "or to cause that person to do any act which he is not legally bound to do, or to omit to do any act which that person is legally entitled to do, "
                    "commits criminal intimidation. Punishment: imprisonment up to two years, or fine, or both. Corresponds to erstwhile IPC Section 503-506."
                ),
            },
            {
                "section": "74",
                "text": (
                    "BNS Section 74 — Assault or criminal force to woman with intent to outrage her modesty. "
                    "Whoever assaults or uses criminal force to any woman, intending to outrage or knowing it to be likely that he will thereby outrage her modesty, "
                    "shall be punished with imprisonment of either description for a term which shall not be less than one year but which may extend to five years, and shall also be liable to fine. "
                    "Corresponds to erstwhile IPC Section 354."
                ),
            },
            {
                "section": "115",
                "text": (
                    "BNS Section 115 — Voluntarily causing hurt. Whoever does any act with the intention of thereby causing hurt to any person, "
                    "or with the knowledge that he is likely thereby to cause hurt to any person, and does thereby cause hurt to any person, "
                    "is said to voluntarily cause hurt. Punishment: imprisonment up to one year, or fine up to ten thousand rupees, or both. "
                    "Corresponds to erstwhile IPC Section 323."
                ),
            },
            {
                "section": "117",
                "text": (
                    "BNS Section 117 — Voluntarily causing grievous hurt. Whoever voluntarily causes hurt, "
                    "if the hurt which he intends to cause or knows himself to be likely to cause is grievous hurt, "
                    "and if the hurt which he causes is grievous hurt, is said to voluntarily cause grievous hurt. "
                    "Punishment: imprisonment up to seven years, and fine. Corresponds to erstwhile IPC Section 325."
                ),
            },
        ],
    },
    # --- BNSS (Bharatiya Nagarik Suraksha Sanhita, 2023) — replaces CrPC ---
    {
        "title": "Bharatiya Nagarik Suraksha Sanhita, 2023 (BNSS)",
        "source_type": "statute",
        "authority_level": "central_statute",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/19808",
        "source_domain": "indiacode.nic.in",
        "act_name": "Bharatiya Nagarik Suraksha Sanhita, 2023",
        "language": "en",
        "chunks": [
            {
                "section": "173",
                "text": (
                    "BNSS Section 173 — Information in cognizable cases (FIR). "
                    "Every information relating to the commission of a cognizable offence, if given orally to an officer in charge of a police station, "
                    "shall be reduced to writing by him or under his direction, and be read over to the informant; and every such information, "
                    "whether given in writing or reduced to writing as aforesaid, shall be signed by the person giving it, "
                    "and the substance thereof shall be entered in a book to be kept by such officer in such form as the State Government may prescribe in this behalf. "
                    "A copy of the information as recorded shall be given forthwith, free of cost, to the informant. "
                    "This is the procedure for filing a First Information Report (FIR). "
                    "Corresponds to erstwhile CrPC Section 154. "
                    "IMPORTANT: The police officer MUST register the FIR if the information discloses a cognizable offence. "
                    "Refusal to register FIR is itself an offence. If police refuse, complaint can be sent to the Superintendent of Police or a Magistrate under Section 175 BNSS."
                ),
            },
            {
                "section": "175",
                "text": (
                    "BNSS Section 175 — Procedure when police officer refuses to register FIR. "
                    "If an officer in charge of a police station refuses to record the information referred to in Section 173, "
                    "the informant may send the substance of such information, in writing and by post, to the Superintendent of Police concerned "
                    "who, if satisfied that such information discloses the commission of a cognizable offence, shall either investigate the case himself "
                    "or direct an investigation to be made by any police officer subordinate to him. "
                    "Alternatively, the informant can approach the Magistrate under Section 223 BNSS. "
                    "Corresponds to erstwhile CrPC Section 154(3)."
                ),
            },
            {
                "section": "480",
                "text": (
                    "BNSS Section 480 — Bail in non-bailable offences. "
                    "When any person accused of, or suspected of, the commission of any non-bailable offence is arrested or detained without warrant by an officer in charge of a police station "
                    "or appears or is brought before a Court other than the High Court or Court of Session, he may be released on bail. "
                    "But he shall not be so released if there appear reasonable grounds for believing that he has been guilty of an offence punishable with death or imprisonment for life. "
                    "The Court shall consider the nature and gravity of the accusation, antecedents of the applicant, possibility of the applicant fleeing from justice, "
                    "and whether the accusation has been made with the object of injuring or humiliating the applicant. "
                    "For offences punishable with imprisonment up to 7 years, if the accused has been in custody for half of the maximum sentence, bail shall be granted. "
                    "Corresponds to erstwhile CrPC Section 437."
                ),
            },
            {
                "section": "482",
                "text": (
                    "BNSS Section 482 — Anticipatory bail. "
                    "When any person has reason to believe that he may be arrested on accusation of having committed a non-bailable offence, "
                    "he may apply to the High Court or the Court of Session for a direction that in the event of such arrest he shall be released on bail. "
                    "The Court may grant anticipatory bail with conditions including: "
                    "(i) the person shall make himself available for interrogation by the police officer as and when required; "
                    "(ii) the person shall not, directly or indirectly, make any inducement, threat or promise to any person acquainted with the facts of the case; "
                    "(iii) the person shall not leave India without the previous permission of the Court. "
                    "Corresponds to erstwhile CrPC Section 438."
                ),
            },
            {
                "section": "479",
                "text": (
                    "BNSS Section 479 — When bail may be taken in case of bailable offence. "
                    "When any person other than a person accused of a non-bailable offence is arrested or detained without warrant by an officer in charge of a police station, "
                    "or appears or is brought before a Court, and is prepared at any time while in the custody of such officer or at any stage of the proceeding before such Court "
                    "to give bail, such person shall be released on bail. "
                    "Bail is a RIGHT in bailable offences — the police or court MUST grant bail. "
                    "Corresponds to erstwhile CrPC Section 436."
                ),
            },
            {
                "section": "193",
                "text": (
                    "BNSS Section 193 — Charge sheet / Police report on completion of investigation. "
                    "Every investigation shall be completed without unnecessary delay and the report shall be forwarded to the Magistrate. "
                    "The report shall set forth the names of the parties, the nature of the information, the names of the persons who appear to be acquainted with the circumstances of the case, "
                    "and whether the accused has been arrested and released on bail, whether released on his bond with or without sureties, "
                    "whether sent in custody, and whether the offence appears to have been committed. "
                    "If investigation is not completed within 60 days (where imprisonment may extend to less than 10 years) or 90 days (where imprisonment may extend to 10 years or more), "
                    "the accused shall be released on bail. This is known as 'default bail'. "
                    "Corresponds to erstwhile CrPC Section 173."
                ),
            },
            {
                "section": "210",
                "text": (
                    "BNSS Section 210 — Commencement of trial. "
                    "In every inquiry or trial, the proceedings shall be held as expeditiously as possible, and in particular, "
                    "when the examination of witnesses has once begun, the same shall be continued from day to day until all the witnesses in attendance have been examined. "
                    "Adjournments: No adjournment shall be granted without recording reasons in writing. "
                    "Maximum two adjournments may be granted to a party at the stage of hearing of arguments. "
                    "Corresponds to erstwhile CrPC Section 309."
                ),
            },
            {
                "section": "223",
                "text": (
                    "BNSS Section 223 — Complaint to Magistrate. "
                    "Any person aggrieved by an offence may make a complaint to a Judicial Magistrate. "
                    "A complaint may be made orally or in writing. If oral, the Magistrate shall reduce it to writing. "
                    "The Magistrate shall then examine the complainant and witnesses on oath. "
                    "If there is sufficient ground for proceeding, the Magistrate shall issue process against the accused. "
                    "This is an alternative remedy when police refuse to register FIR. "
                    "Corresponds to erstwhile CrPC Section 200."
                ),
            },
            {
                "section": "530",
                "text": (
                    "BNSS Section 530 — Inherent powers of High Court. "
                    "Nothing in this Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary "
                    "to give effect to any order under this Sanhita, or to prevent abuse of the process of any Court or otherwise to secure the ends of justice. "
                    "This section is invoked for quashing of FIRs, quashing of criminal proceedings, and for exercising extraordinary jurisdiction. "
                    "Corresponds to erstwhile CrPC Section 482."
                ),
            },
        ],
    },
    # --- BSA (Bharatiya Sakshya Adhiniyam, 2023) — replaces Indian Evidence Act ---
    {
        "title": "Bharatiya Sakshya Adhiniyam, 2023 (BSA)",
        "source_type": "statute",
        "authority_level": "central_statute",
        "source_url": "https://www.indiacode.nic.in/handle/123456789/19809",
        "source_domain": "indiacode.nic.in",
        "act_name": "Bharatiya Sakshya Adhiniyam, 2023",
        "language": "en",
        "chunks": [
            {
                "section": "1",
                "text": (
                    "BSA Section 1 — Short title, commencement and application. "
                    "This Adhiniyam may be called the Bharatiya Sakshya Adhiniyam, 2023. "
                    "It replaces the Indian Evidence Act, 1872 effective 1 July 2024. "
                    "It applies to all judicial proceedings in or before any Court. "
                    "Key changes include recognition of electronic and digital evidence on par with physical evidence."
                ),
            },
            {
                "section": "57",
                "text": (
                    "BSA Section 57 — Admissibility of electronic records. "
                    "Any information contained in an electronic record which is printed on a paper, stored, recorded or copied in optical or magnetic media "
                    "produced by a computer shall be deemed to be also a document. "
                    "Electronic records are admissible as evidence if the computer producing it was in regular use, "
                    "the information was regularly fed into the computer in the ordinary course of activities, "
                    "and the output is produced during the period over which the computer was used regularly. "
                    "A certificate identifying the electronic record and describing the manner in which it was produced shall be evidence of any matter stated in the certificate. "
                    "Corresponds to erstwhile Evidence Act Section 65B."
                ),
            },
            {
                "section": "39",
                "text": (
                    "BSA Section 39 — Confession. A confession made by an accused person is irrelevant in a criminal proceeding, "
                    "if the making of the confession appears to the Court to have been caused by any inducement, threat or promise. "
                    "A confession made to a police officer shall not be proved as against a person accused of any offence. "
                    "A confession made by any person whilst he is in the custody of a police officer, unless it be made in the immediate presence of a Magistrate, shall not be proved. "
                    "Corresponds to erstwhile Evidence Act Sections 24-26."
                ),
            },
        ],
    },
    # --- Constitution of India — Fundamental Rights ---
    {
        "title": "Constitution of India — Fundamental Rights",
        "source_type": "statute",
        "authority_level": "constitution",
        "source_url": "https://legislative.gov.in/constitution-of-india/",
        "source_domain": "legislative.gov.in",
        "act_name": "Constitution of India",
        "language": "en",
        "chunks": [
            {
                "section": "14",
                "text": (
                    "Article 14 — Equality before law. The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. "
                    "This article embodies the principle of rule of law and prohibits arbitrary discrimination. "
                    "It permits reasonable classification for the purpose of legislation provided the classification is based on intelligible differentia "
                    "and there is a rational nexus between the differentia and the object sought to be achieved."
                ),
            },
            {
                "section": "19",
                "text": (
                    "Article 19 — Protection of certain rights regarding freedom of speech, etc. "
                    "(1) All citizens shall have the right to: (a) freedom of speech and expression; (b) assemble peaceably and without arms; "
                    "(c) form associations or unions or co-operative societies; (d) move freely throughout the territory of India; "
                    "(e) reside and settle in any part of the territory of India; (g) practise any profession, or to carry on any occupation, trade or business. "
                    "These rights are subject to reasonable restrictions in the interests of sovereignty and integrity of India, security of the State, "
                    "friendly relations with foreign States, public order, decency or morality, contempt of court, defamation, or incitement to an offence."
                ),
            },
            {
                "section": "20",
                "text": (
                    "Article 20 — Protection in respect of conviction for offences. "
                    "(1) No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act (no ex post facto laws). "
                    "(2) No person shall be prosecuted and punished for the same offence more than once (double jeopardy). "
                    "(3) No person accused of any offence shall be compelled to be a witness against himself (right against self-incrimination)."
                ),
            },
            {
                "section": "21",
                "text": (
                    "Article 21 — Protection of life and personal liberty. No person shall be deprived of his life or personal liberty except according to procedure established by law. "
                    "The Supreme Court has held that the right to life includes the right to live with dignity, right to livelihood, right to health, "
                    "right to clean environment, right to shelter, right to speedy trial, right to legal aid, and right to privacy. "
                    "In Maneka Gandhi v. Union of India (1978), the Supreme Court held that the 'procedure established by law' must be just, fair and reasonable."
                ),
            },
            {
                "section": "21A",
                "text": (
                    "Article 21A — Right to education. The State shall provide free and compulsory education to all children of the age of six to fourteen years "
                    "in such manner as the State may, by law, determine. Inserted by the 86th Constitutional Amendment Act, 2002."
                ),
            },
            {
                "section": "22",
                "text": (
                    "Article 22 — Protection against arrest and detention in certain cases. "
                    "(1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest. "
                    "(2) Every person who is arrested and detained in custody shall be produced before the nearest magistrate within a period of twenty-four hours of such arrest. "
                    "(3) No such person shall be detained in custody beyond the said period without the authority of a magistrate. "
                    "This right to be produced before a magistrate within 24 hours is a fundamental right under the Constitution."
                ),
            },
            {
                "section": "32",
                "text": (
                    "Article 32 — Remedies for enforcement of fundamental rights (Writ Jurisdiction of Supreme Court). "
                    "The right to move the Supreme Court for the enforcement of fundamental rights is itself a fundamental right. "
                    "The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, "
                    "prohibition, quo warranto and certiorari, for the enforcement of any of the rights conferred by Part III of the Constitution. "
                    "Article 226 provides similar power to the High Courts."
                ),
            },
        ],
    },
    # --- Common Legal Procedures ---
    {
        "title": "Legal Procedures — FIR, Bail, Anticipatory Bail, Legal Notice",
        "source_type": "statute",
        "authority_level": "central_statute",
        "source_url": "https://www.indiacode.nic.in/",
        "source_domain": "indiacode.nic.in",
        "act_name": "BNSS/CrPC Procedures",
        "language": "en",
        "chunks": [
            {
                "section": "FIR-process",
                "text": (
                    "PROCEDURE FOR FILING AN FIR (First Information Report) IN INDIA: "
                    "Step 1: Visit the nearest police station having jurisdiction over the area where the offence occurred. "
                    "Step 2: Provide information about the cognizable offence to the Station House Officer (SHO) or officer in charge. "
                    "The information can be given orally or in writing. If given orally, the police officer must write it down. "
                    "Step 3: The information will be read over to the informant, who must sign it. "
                    "Step 4: The officer enters the substance in the Station Diary / Daily Register and assigns an FIR number. "
                    "Step 5: The informant MUST be given a free copy of the FIR immediately. "
                    "IMPORTANT: Under Section 173 BNSS (formerly Section 154 CrPC), the police MUST register an FIR if the information discloses a cognizable offence. "
                    "If police refuse to register FIR: (a) Send written complaint to Superintendent of Police under Section 175 BNSS; "
                    "(b) File a complaint before a Judicial Magistrate under Section 223 BNSS; "
                    "(c) File a writ petition in the High Court; (d) Register Zero FIR at any police station (it will be transferred to the jurisdictional police station). "
                    "E-FIR: Many states now allow filing of FIRs online through their respective police portals."
                ),
            },
            {
                "section": "bail-process",
                "text": (
                    "PROCEDURE FOR OBTAINING BAIL IN INDIA: "
                    "Bail in Bailable Offences (Section 479 BNSS / Section 436 CrPC): Bail is a matter of RIGHT. "
                    "The accused can demand bail from the police station itself or from the court. The police officer or court MUST grant bail. "
                    "Bail in Non-Bailable Offences (Section 480 BNSS / Section 437 CrPC): Bail is at the discretion of the court. "
                    "Step 1: File a bail application before the appropriate court (usually the court where the case is pending). "
                    "Step 2: The application must state grounds for bail — nature of accusation, severity of punishment, character of evidence, "
                    "reasonable apprehension of tampering with evidence or influencing witnesses, and prima facie satisfaction of the court. "
                    "Step 3: The court considers: (a) nature and gravity of the accusation; (b) antecedents of the applicant; "
                    "(c) possibility of fleeing justice; (d) possibility of tampering with evidence. "
                    "Step 4: If bail is granted, the accused must furnish a bail bond with sureties as directed by the court. "
                    "Default Bail (Section 193 BNSS / Section 167(2) CrPC): If investigation is not completed within 60 days (for offences with max punishment less than 10 years) "
                    "or 90 days (for offences with max punishment 10 years or more), the accused has an indefeasible RIGHT to bail."
                ),
            },
            {
                "section": "anticipatory-bail-process",
                "text": (
                    "PROCEDURE FOR ANTICIPATORY BAIL IN INDIA (Section 482 BNSS / Section 438 CrPC): "
                    "Anticipatory bail is a direction to release a person on bail in the event of arrest for a non-bailable offence. "
                    "Step 1: Engage a lawyer to draft the anticipatory bail application. "
                    "Step 2: File the application before the Court of Session or the High Court. "
                    "Step 3: The application must state the reason to believe that arrest may happen, the nature of the accusation, "
                    "and grounds why bail should be granted. "
                    "Step 4: The court may impose conditions: (a) availability for interrogation; (b) not making inducements or threats to witnesses; "
                    "(c) not leaving India without court permission; (d) any other condition the court deems fit. "
                    "The Supreme Court in Sushila Aggarwal v. State (NCT of Delhi) (2020) held that anticipatory bail can be granted without any time limit "
                    "and the protection shall continue until the end of the trial unless the court specifically sets a time limit."
                ),
            },
            {
                "section": "legal-notice-process",
                "text": (
                    "PROCEDURE FOR SENDING A LEGAL NOTICE IN INDIA: "
                    "A legal notice is a formal communication sent by a person or their lawyer to another person or entity, "
                    "informing them of a grievance and demanding certain action or remedy. "
                    "Step 1: Consult a lawyer to draft the legal notice. "
                    "Step 2: The notice should clearly state: (a) facts of the dispute; (b) legal basis; "
                    "(c) demand or relief sought; (d) time limit for compliance (usually 15-30 days); "
                    "(e) consequences of non-compliance (filing a suit, criminal complaint, etc.). "
                    "Step 3: Send the notice through Registered Post with Acknowledgement Due (RPAD) or through a lawyer. "
                    "Step 4: Keep proof of dispatch (postal receipt) and delivery (acknowledgement card). "
                    "IMPORTANT: Under Section 80 of the Code of Civil Procedure, a legal notice of 60 days is mandatory before filing a suit against the Government or a public officer. "
                    "Under the Negotiable Instruments Act, a notice of 30 days under Section 138 is mandatory before filing a complaint for cheque bounce."
                ),
            },
            {
                "section": "writ-petition-process",
                "text": (
                    "WRIT PETITION IN INDIA (Articles 32 and 226 of the Constitution): "
                    "Writs are constitutional remedies to enforce fundamental rights. "
                    "Types of Writs: "
                    "(1) Habeas Corpus — to produce a person detained unlawfully before the court. Filed when someone is illegally detained or arrested. "
                    "(2) Mandamus — to command a public authority to perform a duty it has failed to perform. "
                    "(3) Certiorari — to quash an order passed by a lower court or tribunal acting beyond its jurisdiction. "
                    "(4) Prohibition — to prevent a lower court or tribunal from exceeding its jurisdiction. "
                    "(5) Quo Warranto — to question the authority of a person holding public office. "
                    "Article 32: Writ petition before the Supreme Court for enforcement of fundamental rights. "
                    "Article 226: Writ petition before the High Court — broader scope, can be filed for enforcement of fundamental rights AND for any other purpose. "
                    "Filing: A writ petition can be filed by any person whose fundamental rights are violated (under Article 32) "
                    "or by any aggrieved person (under Article 226). PIL (Public Interest Litigation) can be filed by any public-spirited person."
                ),
            },
            {
                "section": "cheque-bounce",
                "text": (
                    "CHEQUE BOUNCE / DISHONOUR OF CHEQUE (Section 138, Negotiable Instruments Act, 1881): "
                    "When a cheque drawn by a person is returned unpaid (bounced) due to insufficiency of funds, it is an offence. "
                    "Procedure: Step 1: The payee must send a legal notice to the drawer within 30 days of receiving information of dishonour from the bank. "
                    "Step 2: The notice must demand payment of the cheque amount within 15 days of receipt of notice. "
                    "Step 3: If the drawer fails to pay within 15 days, the payee can file a criminal complaint before the Magistrate within 30 days of the expiry of the 15-day period. "
                    "Punishment: Imprisonment up to two years, or fine up to twice the cheque amount, or both. "
                    "The complaint must be filed in the court having jurisdiction over the place where the cheque was presented for encashment. "
                    "Limitation: The complaint must be filed within one month of the cause of action arising (i.e., 30 days after expiry of the 15-day notice period)."
                ),
            },
            {
                "section": "limitation-period",
                "text": (
                    "LIMITATION PERIODS IN INDIAN LAW (Limitation Act, 1963): "
                    "Every suit, appeal, and application must be filed within the prescribed limitation period. "
                    "Key periods: "
                    "(1) Suit for recovery of money lent: 3 years from the date the loan becomes due. "
                    "(2) Suit based on a written contract: 3 years from when the right to sue accrues. "
                    "(3) Suit for possession of immovable property: 12 years from when possession becomes adverse. "
                    "(4) Appeal from a decree of any court: 30 days (High Court) or 90 days (other courts). "
                    "(5) Criminal complaint for cheque bounce (Section 138 NI Act): within 1 month of cause of action. "
                    "(6) Motor accident claim: within 6 months of the accident (can be condoned). "
                    "(7) Consumer complaint: within 2 years from the date of cause of action. "
                    "The court may condone delay if the applicant shows sufficient cause for the delay. "
                    "Once limitation expires, the right to sue is barred and the court cannot entertain the suit (Section 3, Limitation Act)."
                ),
            },
            {
                "section": "consumer-complaint",
                "text": (
                    "CONSUMER COMPLAINT (Consumer Protection Act, 2019): "
                    "Any consumer who has purchased goods or hired services can file a complaint for deficiency in service or defective goods. "
                    "Forums: (1) District Consumer Disputes Redressal Commission — for claims up to Rs. 1 crore. "
                    "(2) State Consumer Disputes Redressal Commission — for claims between Rs. 1 crore and Rs. 10 crore. "
                    "(3) National Consumer Disputes Redressal Commission (NCDRC) — for claims exceeding Rs. 10 crore. "
                    "The complaint can be filed online through the E-Daakhil portal (edaakhil.nic.in). "
                    "Limitation: 2 years from the date of cause of action. "
                    "No court fee is required for claims up to Rs. 5 lakh. "
                    "The complaint must include: name and address of complainant and opposite party, facts of the complaint, "
                    "relief sought, and supporting documents."
                ),
            },
            {
                "section": "domestic-violence",
                "text": (
                    "PROTECTION FROM DOMESTIC VIOLENCE (Protection of Women from Domestic Violence Act, 2005): "
                    "Any woman who is subjected to domestic violence (physical, sexual, verbal, emotional, or economic abuse) "
                    "can seek protection under this Act. "
                    "Remedies available: (1) Protection Order (Section 18) — prohibiting the respondent from committing domestic violence. "
                    "(2) Residence Order (Section 19) — preventing the respondent from dispossessing the aggrieved person from the shared household. "
                    "(3) Monetary Relief (Section 20) — compensation for expenses, loss of earnings, medical expenses, etc. "
                    "(4) Custody Order (Section 21) — temporary custody of children. "
                    "How to file: File an application before the Magistrate (Judicial Magistrate First Class or Metropolitan Magistrate). "
                    "The Protection Officer or a Service Provider can assist in filing. "
                    "The complaint can also be lodged at the nearest police station."
                ),
            },
            {
                "section": "remand",
                "text": (
                    "REMAND IN INDIAN LAW (Section 187 BNSS / Section 167 CrPC): "
                    "When an accused is arrested and the investigation cannot be completed within 24 hours, "
                    "the police must produce the accused before the nearest Judicial Magistrate. "
                    "The Magistrate may authorize detention of the accused in custody (judicial or police) for a term not exceeding 15 days at a time. "
                    "Police custody (police remand): Maximum 15 days from the date of first remand. Used for custodial interrogation. "
                    "Judicial custody (judicial remand): Beyond police custody, the accused is sent to jail. Can be extended up to 60 or 90 days. "
                    "After 60 days (offence punishable with less than 10 years) or 90 days (offence punishable with 10 years or more), "
                    "if charge sheet is not filed, the accused has an INDEFEASIBLE RIGHT to default bail under Section 193 BNSS."
                ),
            },
        ],
    },
]


def seed():
    conn = psycopg.connect(DATABASE_URL, row_factory=dict_row)
    cur = conn.cursor()

    # Clear old junk chunks (navigation text)
    cur.execute("DELETE FROM legal_source_chunks")
    conn.commit()
    print("Cleared existing chunks.")

    total_chunks = 0

    for source_def in SOURCES:
        chunks = source_def.pop("chunks")

        # Upsert the source
        cur.execute(
            """
            INSERT INTO legal_sources (title, source_type, authority_level, source_url, source_domain, act_name, language, verification_status, index_status)
            VALUES (%(title)s, %(source_type)s, %(authority_level)s, %(source_url)s, %(source_domain)s, %(act_name)s, %(language)s, 'verified', 'indexed')
            RETURNING id
            """,
            source_def,
        )
        source_id = cur.fetchone()["id"]

        for idx, chunk in enumerate(chunks):
            text = chunk["text"]
            section = chunk["section"]
            normalized = text.lower()
            token_count = len(text.split())

            act_name = source_def.get("act_name", "")
            label = f"[{act_name}] Section {section} -> {source_def.get('source_url', '')}"

            cur.execute(
                """
                INSERT INTO legal_source_chunks (source_id, chunk_index, chunk_text, normalized_text, token_count, citation_label, section_number, metadata)
                VALUES (%(source_id)s, %(chunk_index)s, %(chunk_text)s, %(normalized_text)s, %(token_count)s, %(citation_label)s, %(section_number)s, %(metadata)s)
                """,
                {
                    "source_id": source_id,
                    "chunk_index": idx + 1,
                    "chunk_text": text,
                    "normalized_text": normalized,
                    "token_count": token_count,
                    "citation_label": label,
                    "section_number": section,
                    "metadata": "{}",
                },
            )
            total_chunks += 1

        conn.commit()
        print(f"  Seeded {len(chunks)} chunks for: {source_def['title']}")

    print(f"\nDone. Total: {total_chunks} chunks across {len(SOURCES)} sources.")
    conn.close()


if __name__ == "__main__":
    seed()
