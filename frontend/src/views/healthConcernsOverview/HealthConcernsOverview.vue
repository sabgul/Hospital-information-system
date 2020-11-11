<template>
    <div>
        <div class="main__content">
            <h1 class="patients__header">
                My health concerns
            </h1>

            <p>
                All your health concerns are shown in table below.<br>
                To show more details about particular concern expand given table row.
            </p>
        </div>

        <div
            v-for="concern in concerns"
            :key="concern.id"
        >
            <div class="concern__content">
                <h4>
                    {{ concern.name }}
                </h4>

                <p>
                    {{ concern.description }}
                </p>

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

            return 'Unknown state';
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

    .concern__content {
      padding: 20px 20px 20px 25px;
      margin: 20px 15% 20px 25%;
      background-color: #ffffff;
        box-shadow:
            0 1.3px 20.1px rgba(0, 0, 0, 0.003),
            0 4.2px 44.8px rgba(0, 0, 0, 0.003),
            0 19px 76px rgba(0, 0, 0, 0.06);
        border-radius: 10px;
    }

    .h4 {
        font-weight: 900;
    }
</style>