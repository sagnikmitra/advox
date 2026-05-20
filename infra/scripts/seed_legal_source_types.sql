-- Placeholder seed for product-level registry values and constants.
-- Includes persona labels, disclaimer text, transition date, and mapping placeholders.
SELECT 'layman' AS persona
UNION ALL
SELECT 'advocate';

SELECT 'LEGAL_TRANSITION_DATE' AS key, '2024-07-01' AS value;
SELECT 'DISCLAIMER' AS key,
'LEGAL DISCLAIMER: This AI agent provides legal information and procedural guidance based on the Indian legal framework, including BNS, BNSS, and BSA where applicable. It does not constitute formal legal advice, representation, or an attorney-client relationship. AI performance can vary; verify all critical citations, deadlines, and strategies with a certified legal practitioner before acting.' AS value;

SELECT 'criminal_mapping_placeholder' AS key, 'IPC->BNS, CrPC->BNSS, Evidence Act->BSA' AS value;
