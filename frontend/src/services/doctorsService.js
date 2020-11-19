import axios_instance from "@/http-common";

class DoctorsService {
  getAll() {
    return axios_instance.get("api/doctors");
  }

  get(id) {
    return axios_instance.get(`api/doctors/${id}`);
  }

  create(data) {
    return axios_instance.post("api/doctors/", data);
  }

  update(id, data) {
    return axios_instance.put(`api/doctors/${id}/`, data);
  }

  delete(id) {
    return axios_instance.delete(`api/doctors/${id}/`);
  }

  deleteAll() {
    return axios_instance.delete(`api/doctors`);
  }
}

export default new DoctorsService();
