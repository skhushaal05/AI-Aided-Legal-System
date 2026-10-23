function Status() {
  return (
    <div className="simple-page">
      <div className="simple-page-content">

        <p className="eyebrow">
          COMPLAINT STATUS
        </p>

        <h1>
          Know where your
          <br />
          complaint stands.
        </h1>

        <p>
          Track the current status and progress
          of your submitted complaint.
        </p>

        <div className="simple-page-rule"></div>

        <div className="status-box">

          <div className="status-item">
            <span className="status-label">
              CURRENT STATUS
            </span>

            <strong>
              No complaint submitted
            </strong>
          </div>

          <div className="status-item">
            <span className="status-label">
              REFERENCE
            </span>

            <strong>
              —
            </strong>
          </div>

        </div>

      </div>
    </div>
  );
}

export default Status;