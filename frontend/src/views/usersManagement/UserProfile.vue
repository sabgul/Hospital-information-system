<template>
    <div class="main__content">
        <h1>Add new examination action</h1>
        <p>
            By adding new examination action, doctors can use them when examinating their patients. <br>
            Thanks to that, you will be able to track unpaid examinations of patients.
        </p>
    </div>
</template>


<script>

export default {
    name: 'UserProfile', 
    
    props: {
        id: Number, 
        role: String
    },

    components: {
    },
    
    data:() => ({

    }),
    
    async created() {
        console.log(this.id, this.role);
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