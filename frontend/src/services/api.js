import axios from "axios";

const BASE_URL = "http://127.0.0.1:8000";

export const getMetrics = async () => {
  const res = await axios.get(`${BASE_URL}/metrics`);
  return res.data;
};

export const getEDAImages = async () => {
  const res = await axios.get(`${BASE_URL}/eda-images`);
  return res.data.charts;
};

export const predictCustomer = async (data) => {
  const res = await axios.post(`${BASE_URL}/predict`, data);
  return res.data;
};