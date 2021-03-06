import http from "@/http-common";

class HealthConcernsService {
  getAll() {
    return http.get("health-concerns/");
  }

  getAllByCurrentUser(currentUserId) {
      return http.get("/health-concerns/", {
      'params': {
          ...({ 'doctor': currentUserId }),
      }
    })
  }

  getAllByPatient(patientId) {
    return http.get("/health-concerns/", {
      'params': {
          ...({ 'patient': patientId }),
      }
    })
  }

  getFilteredByPatient(patientId, filter) {
    return http.get("/health-concerns/", {
      'params': {
          ...({ 'patient': patientId }),
          ...(filter.state !== -1 ? { 'state': filter.state } : {}),
      }
    })
  }

  getFiltered(filter, currentUserId, role) {
    const patient_name = filter.patient_name;
    const state_of_concern = filter.state_of_concern;

    return http.get("/health-concerns/",{
      'params': {
        ...(patient_name !== -1 ? { 'patient': patient_name } : {}),
        ...(state_of_concern !== -1 ? { 'state': state_of_concern } : {}),
        ...(role === 'doctor' ? { 'doctor': currentUserId } : {})
      }
    })
  }

  get(id) {
    return http.get(`health-concerns/${id}/`);
  }

  create(data) {
    return http.post("health-concerns/", data);
  }

  update(id, data) {
    return http.put(`health-concerns/${id}/`, data);
  }

  delete(id) {
    return http.delete(`health-concerns/${id}/`);
  }

  deleteAll() {
    return http.delete(`health-concerns/`);
  }
}

export default new HealthConcernsService();
