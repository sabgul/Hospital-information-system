import axios_instance from "@/http-common";

class HealthcareWorkersService {
  getAll() {
    return axios_instance.get("api/healthcare-workers/");
  }

  get(id) {
    return axios_instance.get(`api/healthcare-workers/${id}/`);
  }

  create(data) {
    return axios_instance.post("api/healthcare-workers/", data);
  }

  update(id, data) {
    return axios_instance.put(`api/healthcare-workers/${id}/`, data);
  }

  delete(id) {
    return axios_instance.delete(`api/healthcare-workers/${id}/`);
  }

  deleteAll() {
    return axios_instance.delete(`api/healthcare-workers/`);
  }
}

export default new HealthcareWorkersService();
