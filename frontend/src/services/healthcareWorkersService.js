import http from "@/http-common";

class HealthcareWorkersService {
  getAll() {
    return http.get("/healthcare-workers");
  }

  get(id) {
    return http.get(`/healthcare-workers/${id}`);
  }

  create(data) {
    return http.post("/healthcare-workers/", data);
  }

  update(id, data) {
    return http.put(`/healthcare-workers/${id}`, data);
  }

  delete(id) {
    return http.delete(`/healthcare-workers/${id}`);
  }

  deleteAll() {
    return http.delete(`/healthcare-workers`);
  }
}

export default new HealthcareWorkersService();
