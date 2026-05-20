export default function AdminIngestionPage() {
  return (
    <section className="page-shell space-y-4">
      <h1 className="display-serif text-4xl">Admin Ingestion Dashboard</h1>
      <div className="card text-sm text-body">
        Job lifecycle: discovered {"->"} fetched {"->"} parsed {"->"} normalized {"->"} legally_classified {"->"} citation_extracted {"->"} verified {"->"} embedded {"->"} indexed {"->"} available_for_rag.
      </div>
    </section>
  );
}
