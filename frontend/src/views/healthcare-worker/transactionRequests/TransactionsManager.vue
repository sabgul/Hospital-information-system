<template>
  <div>
    <div class="main__content">
        <h1 class="requests__header">Transactions requests management</h1>

        <p>
            During patient examination, there are usually several examination actions.<br>
            Many of them might be paid by patient's healthcare insurance.<br>
            You can see overview of all requests made by doctors, which you are able to manage.
        </p>
    </div>

    <div class="main__content">
        <div v-if="requests.length === 0">
            <h4>No requests to manage</h4>
            <img src="../../../assets/relax.svg" alt="">
        </div>
      
        <div
            v-else
            v-for="(request, index) in requests"
            v-bind:key="index"
            class="request"
        >
          <div style="margin-left: 1em;">
              <span>Request n. <b>{{ request.id }}</b></span>
              <br>
              <span>Patient: <b>{{ request.related_to_patient.user.first_name }} {{ request.related_to_patient.user.last_name }}</b></span>
              <br>
              <span>Examination action: <b>{{ request.examination_action.name }}</b></span>
              <br>
              <span>State: <b>{{ getState(request.request_state) }}</b></span>
          </div>

          <div class="buttons__action">
              <vs-button
                  v-if="request.request_state === 'UD'"
                  success
                  style="padding: 6px 30px"
                  @click="openConfirmationRequest(request)"
              >
                  Cover transaction
              </vs-button>

              <vs-button
                  v-if="request.request_state === 'CD'"
                  danger
                  style="padding: 6px 30px"
                  @click="removeRequest(request)"
              >
                  Remove covered transaction
              </vs-button>
          </div>
        </div>
    </div>

    <vs-dialog
            width="300px"
            v-model="confirmationWindowActive"
        >
            <template #header>
            <h5>
                Are you sure you want to cover selected request?
            </h5>
            </template>

            <template #footer>
                <div class="center">
                    <vs-button
                        @click="coverRequest()"
                        success
                    >
                        Yep, cover it
                    </vs-button>

                    <vs-button
                        @click="abortCovering()"
                        transparent
                    >
                        Abort mission
                    </vs-button>
                </div>
            </template>
        </vs-dialog>
  </div>
</template>

<script>
import TransactionRequestsService from "@/services/transactionRequestsService";
import NotificationsUtils from "@/utils/notificationsUtils";

export default {
    name: 'TransactionsManager',    

    data:() => ({
        requests: [],
        confirmationWindowActive: false,
        requestToCover: {},
    }),

    async created() {
        TransactionRequestsService.getAll()
        .then(response => {
            this.requests = response.data;
        })
    },

    methods: {
        getState(rawState) {
          if(rawState === 'CD') {
            return 'Covered';
          }

          if(rawState === 'UD') {
            return 'Unpaid';
          }

          return '';
        },

        openConfirmationRequest(request) {
            this.confirmationWindowActive = true;
            this.requestToCover = request;
        },

        async coverRequest() {
            let editedRequest = {
                id: this.requestToCover.id,
                examination_action: this.requestToCover.examination_action.name,
                related_to_patient: this.requestToCover.related_to_patient.user.id,
                transaction_approver: this.requestToCover.transaction_approver.user.id,
                request_state: 'CD',
            };

            TransactionRequestsService.update(this.requestToCover.id, editedRequest)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Given action is successfully covered by insurance company.', this.$vs);

                    TransactionRequestsService.getAll()
                      .then(response => {
                          this.requests = response.data;
                      })
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });

        },

        async removeRequest(request) {
            TransactionRequestsService.delete(request.id)
                .then(response => {
                    console.log(response);
                    NotificationsUtils.successPopup('Given action was successfully removed.', this.$vs);

                    TransactionRequestsService.getAll()
                      .then(response => {
                          this.requests = response.data;
                      })
                      .catch(e => {
                          console.log(e);
                      });
                })
                .catch(e => {
                    NotificationsUtils.failPopup(e, this.$vs);
                });
        },

        abortCovering() {
            this.confirmationWindowActive = false;
            this.requestToCover = {};
        }
    },
}
</script>

<style scoped>
    .request {
        background-color: #195bff;
        opacity: 0.95;
        color: white;
        padding: 1em 2em;
        border-radius: 10px;
        margin-bottom: 1em;
        display: flex;
        justify-content:space-between;
    }

    .buttons__action {
        margin-top: 1.2em;
    }

    img {
        display: block;
        margin: 2em auto;
        width: 60%;
    }

    .center {
        float: right;
        padding-bottom: 10px;
    }
</style>