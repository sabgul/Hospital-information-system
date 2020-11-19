import axios_instance from "@/http-common";

class PatientsService {
  getAll() {
    return axios_instance.get("api/patients/");
  }

  getAllByDoctor(doctorId) {
    return axios_instance.get("api/patients/", {
      'params': {
        'mainDoctor': doctorId,
      }
    })
  }

  get(id) {
    return axios_instance.get(`api/patients/${id}`);
  }

  create(data) {
    return axios_instance.post("api/patients/", data);
  }

  update(id, data) {
    return axios_instance.put(`api/patients/${id}`, data);
  }

  delete(id) {
    return axios_instance.delete(`api/patients/${id}`);
  }

  deleteAll() {
    return axios_instance.delete(`api/patients`);
  }
}

export default new PatientsService();
