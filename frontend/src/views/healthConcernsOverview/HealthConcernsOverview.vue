<template>
    <div>
        <div class="main__content">
            <h1 class="patients__header">My health concerns</h1>

            <p>
                All your health concerns are shown in table below.<br>
                To show more details about particular concern expand given table row.
            </p>
        </div>

        <div v-for="concern in concerns" :key="concern.id">
            <div class="concern__content">
                <h4>{{ concern.name }}</h4>
                <p>{{ concern.description }}</p>
                Supervised by: <span>{{ concern.doctor.name }}</span>
                <br>
                State: <span>{{ getState(concern.state) }}</span>
            </div>
        </div>
    </div>
</template>


<script>
import HealthConcernsService from '@/services/healthConcernsService.js';

export default {
    name: 'HealthConcernsOverview',    

    components: {
    },
    
    data:() => ({
        concerns: [],
    }),

    async created() {
        HealthConcernsService.getAll()
            .then(response => {
            this.concerns = response.data;
            })
            .catch(e => {
            console.log(e);
            });
    },
    
    methods: {
        getState(rawState) {
            if(rawState === 'WT') {
                return 'Waiting';
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

            return 'Uknown state';
        }
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

    .concern__content {
        margin: 20px 0;
        padding: 20px 20px 20px 25px;
        margin-left: 25%;
        margin-right: 15%;
        background-color: #fafafa;
        border-radius: 10px;
    }

    .h4 {
        font-weight: 900;
    }
</style>