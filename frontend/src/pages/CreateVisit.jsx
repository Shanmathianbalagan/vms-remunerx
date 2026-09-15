import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import Layout from "../components/Layout";
import {
  searchVisitors,
  createVisitor,
  getLocations,
  createVisit,
} from "../services/api";
import "./Dashboard.css";
import "./CreateVisit.css";

export default function CreateVisit() {
  const navigate = useNavigate();

  const [locations, setLocations] = useState([]);

  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [selectedVisitor, setSelectedVisitor] = useState(null);

  const [showNewVisitorForm, setShowNewVisitorForm] = useState(false);
  const [newVisitor, setNewVisitor] = useState({
    name: "",
    phone: "",
    email: "",
    company: "",
  });

  const [visitDetails, setVisitDetails] = useState({
    location_id: "",
    purpose: "",
    start_date: "",
    end_date: "",
    start_time: "",
    end_time: "",
    notes: "",
  });

  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    getLocations()
      .then(setLocations)
      .catch((err) => setError(err.message));
  }, []);

  async function handleSearch(e) {
    e.preventDefault();
    if (query.trim().length < 2) return;
    setSearching(true);
    setError("");
    try {
      const data = await searchVisitors(query.trim());
      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setSearching(false);
    }
  }

  function selectVisitor(visitor) {
    setSelectedVisitor(visitor);
    setShowNewVisitorForm(false);
    setResults([]);
  }

  async function handleAddNewVisitor(e) {
    e.preventDefault();
    setError("");
    try {
      const visitor = await createVisitor(newVisitor);
      setSelectedVisitor(visitor);
      setShowNewVisitorForm(false);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleCreateVisit(e) {
    e.preventDefault();
    setError("");

    if (!selectedVisitor) {
      setError("Please select or add a visitor first.");
      return;
    }

    setSubmitting(true);
    try {
      const visit = await createVisit({
        visitor_id: selectedVisitor.visitor_id,
        location_id: Number(visitDetails.location_id),
        purpose: visitDetails.purpose,
        start_date: visitDetails.start_date,
        end_date: visitDetails.end_date,
        start_time: visitDetails.start_time,
        end_time: visitDetails.end_time,
        notes: visitDetails.notes || null,
      });
      navigate(`/visits/${visit.visit_id}/invitation`);
    } catch (err) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Layout>
      <h1 className="page-title">Host a Visit</h1>
      <p className="page-subtitle">
        Search or add a visitor, then enter the visit details.
      </p>

      {error && <div className="visits-error">{error}</div>}

      <div className="create-visit-grid">

      <div className="create-visit-section">
        <h2>1. Visitor Details</h2>

        {selectedVisitor ? (
          <div className="selected-visitor">
            <div>
              <strong>{selectedVisitor.name}</strong>
              <div className="selected-visitor-meta">
                {selectedVisitor.phone}
                {selectedVisitor.company ? ` · ${selectedVisitor.company}` : ""}
              </div>
            </div>
            <button
              type="button"
              className="btn-secondary"
              onClick={() => setSelectedVisitor(null)}
            >
              Change
            </button>
          </div>
        ) : (
          <>
            <form className="visitor-search-form" onSubmit={handleSearch}>
              <input
                type="text"
                placeholder="Search by name, phone, or email..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button type="submit" className="btn-secondary">
                {searching ? "Searching..." : "Search"}
              </button>
            </form>

            {results.length > 0 && (
              <ul className="visitor-results">
                {results.map((v) => (
                  <li key={v.visitor_id}>
                    <div>
                      <strong>{v.name}</strong>
                      <div className="selected-visitor-meta">
                        {v.phone}
                        {v.company ? ` · ${v.company}` : ""}
                      </div>
                    </div>
                    <button
                      type="button"
                      className="btn-secondary"
                      onClick={() => selectVisitor(v)}
                    >
                      Select
                    </button>
                  </li>
                ))}
              </ul>
            )}

            {!showNewVisitorForm && (
              <button
                type="button"
                className="btn-link"
                onClick={() => setShowNewVisitorForm(true)}
              >
                + Add New Visitor
              </button>
            )}

            {showNewVisitorForm && (
              <form className="new-visitor-form" onSubmit={handleAddNewVisitor}>
                <div className="form-row">
                  <label>Visitor Name *</label>
                  <input
                    type="text"
                    required
                    value={newVisitor.name}
                    onChange={(e) =>
                      setNewVisitor({ ...newVisitor, name: e.target.value })
                    }
                  />
                </div>
                <div className="form-row">
                  <label>Phone Number *</label>
                  <input
                    type="text"
                    required
                    value={newVisitor.phone}
                    onChange={(e) =>
                      setNewVisitor({ ...newVisitor, phone: e.target.value })
                    }
                  />
                </div>
                <div className="form-row">
                  <label>Email</label>
                  <input
                    type="email"
                    value={newVisitor.email}
                    onChange={(e) =>
                      setNewVisitor({ ...newVisitor, email: e.target.value })
                    }
                  />
                </div>
                <div className="form-row">
                  <label>Company</label>
                  <input
                    type="text"
                    value={newVisitor.company}
                    onChange={(e) =>
                      setNewVisitor({ ...newVisitor, company: e.target.value })
                    }
                  />
                </div>
                <button type="submit" className="btn-primary">
                  Save Visitor
                </button>
              </form>
            )}
          </>
        )}
      </div>

      <div className="create-visit-section">
        <h2>2. Visit Details</h2>
        <form className="visit-details-form" onSubmit={handleCreateVisit}>
          <div className="form-row">
            <label>Purpose *</label>
            <input
              type="text"
              required
              value={visitDetails.purpose}
              onChange={(e) =>
                setVisitDetails({ ...visitDetails, purpose: e.target.value })
              }
            />
          </div>

          <div className="form-row">
            <label>Location *</label>
            <select
              required
              value={visitDetails.location_id}
              onChange={(e) =>
                setVisitDetails({ ...visitDetails, location_id: e.target.value })
              }
            >
              <option value="">Select a location</option>
              {locations.map((loc) => (
                <option key={loc.location_id} value={loc.location_id}>
                  {loc.name}
                </option>
              ))}
            </select>
          </div>

          <div className="form-row-group">
            <div className="form-row">
              <label>Start Date *</label>
              <input
                type="date"
                required
                value={visitDetails.start_date}
                onChange={(e) =>
                  setVisitDetails({ ...visitDetails, start_date: e.target.value })
                }
              />
            </div>
            <div className="form-row">
              <label>End Date *</label>
              <input
                type="date"
                required
                min={visitDetails.start_date || undefined}
                value={visitDetails.end_date}
                onChange={(e) =>
                  setVisitDetails({ ...visitDetails, end_date: e.target.value })
                }
              />
            </div>
          </div>

          <div className="form-row-group">
            <div className="form-row">
              <label>Start Time *</label>
              <input
                type="time"
                required
                value={visitDetails.start_time}
                onChange={(e) =>
                  setVisitDetails({ ...visitDetails, start_time: e.target.value })
                }
              />
            </div>
            <div className="form-row">
              <label>End Time *</label>
              <input
                type="time"
                required
                value={visitDetails.end_time}
                onChange={(e) =>
                  setVisitDetails({ ...visitDetails, end_time: e.target.value })
                }
              />
            </div>
          </div>

          <div className="form-row">
            <label>Notes</label>
            <textarea
              rows="3"
              value={visitDetails.notes}
              onChange={(e) =>
                setVisitDetails({ ...visitDetails, notes: e.target.value })
              }
            ></textarea>
          </div>

          <button type="submit" className="btn-primary" disabled={submitting}>
            {submitting ? "Creating..." : "Create Visit"}
          </button>
        </form>
      </div>

      </div>
    </Layout>
  );
}
