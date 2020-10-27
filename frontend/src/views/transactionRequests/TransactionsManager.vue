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

    components: {
    },

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

    methods: {
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
        margin-left: 25%;
        margin-right: 15%;
        background-color: #fafafa;
        border-radius: 10px;
    }
</style>