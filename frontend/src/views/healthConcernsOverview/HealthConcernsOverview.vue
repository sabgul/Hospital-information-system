<template>
    <div>
        <div class="main__content">
            <h1 class="patients__header">My health concerns</h1>

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
    .main__content {
        padding: 20px 20px 20px 280px;
        margin-left: 15%;
        margin-right: 15%;
    }

    .concern__content {
        background-color: #fafafa;
        border-radius: 10px;
        padding: 20px; 
        margin: 20px 0;
    }

    .h4 {
        font-weight: 900;
    }
</style>