import Layout from "../components/Layout";
import "./Dashboard.css";

export default function ComingSoon({ title }) {
  return (
    <Layout>
      <h1 className="page-title">{title}</h1>
      <p className="page-subtitle">This module will be built in an upcoming phase.</p>
    </Layout>
  );
}
