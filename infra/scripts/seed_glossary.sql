INSERT INTO legal_glossary (canonical_term, english_term, hindi_term, bengali_term, plain_language_explanation, technical_definition, related_statutes)
VALUES
('cognizable_offence', 'Cognizable offence', 'संज्ञेय अपराध', 'আমলযোগ্য অপরাধ', 'Police can generally register FIR and investigate without prior Magistrate permission.', 'A legally cognizable criminal offence category under applicable criminal procedure.', ARRAY['BNSS', 'CrPC'])
ON CONFLICT DO NOTHING;
