function Products() {
  return (
    <div className="simple-page">

      <main className="simple-page-content">

        <p className="eyebrow">
          POSH PRODUCTS
        </p>

        <h1>
          Tools for a
          <br />
          safer workplace.
        </h1>

        <p>
          Explore the tools available through the
          POSH platform for workplace safety,
          legal awareness and complaint management.
        </p>

        <div className="simple-page-rule"></div>

        <div className="product-feature">
          <span>01</span>

          <div>
            <h3>Law Chatbot</h3>

            <p>
              Ask questions about POSH law and
              access understandable legal information
              through the platform.
            </p>
          </div>
        </div>

        <div className="product-feature">
          <span>02</span>

          <div>
            <h3>Complaints</h3>

            <p>
              Submit workplace complaints through
              a structured digital complaint workflow.
            </p>
          </div>
        </div>

        <div className="product-feature">
          <span>03</span>

          <div>
            <h3>Complaint Status</h3>

            <p>
              Track the current status and progress
              of a submitted complaint.
            </p>
          </div>
        </div>

      </main>

    </div>
  );
}

export default Products;