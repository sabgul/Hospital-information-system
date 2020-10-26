import http from "@/http-common";

class HealthConcernsService {
  getAll() {
    return http.get("/health-concerns");
  }

  get(id) {
    return http.get(`/health-concerns/${id}`);
  }

  create(data) {
    return http.post("/health-concerns/", data);
  }

  update(id, data) {
    return http.put(`/health-concerns/${id}`, data);
  }

  delete(id) {
    return http.delete(`/health-concerns/${id}`);
  }

  deleteAll() {
    return http.delete(`/health-concerns`);
  }
}

export default new HealthConcernsService();
