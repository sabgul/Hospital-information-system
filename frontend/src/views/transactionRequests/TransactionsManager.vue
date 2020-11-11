<template>
  <div>
    <div class="main__content">
        <h1 class="requests__header">Transactions requests management</h1>

        <p>
            During patient examination, there are usually several examination actions.<br>
            Many of them might be paid by patient's healthcare insurence.<br>
            You can see overview of all requests made by doctors, which you are able to manage.
        </p>
    </div>
  </div>
</template>

<script>
import TransactionRequestsService from "@/services/transactionRequestsService";

export default {
    name: 'TransactionsManager',    

    data:() => ({
        requests: [],
    }),

    async created() {
        TransactionRequestsService.getAll()
        .then(response => {
            this.requests = response.data;
        })
        .catch(e => {
            console.log(e);
        });
    },
}
</script>

<style scoped>
    h1 {
        margin-top: 0.5em;
        margin-bottom: 1em;
    }

    .main__content {
        padding: 20px 20px 20px 25px;
        margin-top: 20px;
        margin-left: 25%;
        margin-right: 15%;
        background-color: #ffffff;
        box-shadow:
            0 1.3px 20.1px rgba(0, 0, 0, 0.003),
            0 4.2px 44.8px rgba(0, 0, 0, 0.003),
            0 19px 76px rgba(0, 0, 0, 0.06);
        border-radius: 10px;
    }
</style>