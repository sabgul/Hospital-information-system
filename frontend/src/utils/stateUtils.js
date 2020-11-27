class StateUtils {
    getExaminationState(rawState) {
          if(rawState === 'WT') {
              return 'Waiting for first examination';
          }

          if(rawState === 'ON') {
              return 'Ongoing';
          }

          if(rawState === 'TL') {
              return 'Terminal';
          }

          if(rawState === 'ED') {
              return 'Ended';
          }

          return 'Unknown state';
    }

    getTicketState(rawState) {
        if(rawState === 'PD') {
            return 'Ticket is waiting. Examine your patient!';
        }

        if(rawState === 'CD') {
            return 'Examination request was canceled.';
        }

        if(rawState === 'RD') {
            return 'Ticket already resolved.';
        }

        return 'Undefined state';
    }

    getTransactionState(rawState) {
        if(rawState === 'CD') {
            return 'Covered';
          }

          if(rawState === 'UD') {
            return 'Unpaid';
          }

          return 'Undefined state';
    }

    getGenderState(rawGender) {
        if(rawGender === 'M') {
          return 'Male';
        }

        if(rawGender === 'F') {
          return 'Female';
        }

        if(rawGender === 'O') {
          return 'Other';
        }

        return 'Undefined gender';
    }
}

export default new StateUtils();