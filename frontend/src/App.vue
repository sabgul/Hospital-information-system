<template>
  <div id="app">
    <div v-if="this.$route.path !== '/'">
      <vs-sidebar
      v-model="active"
      open
      >
        <template #logo>

            <img src="./assets/hospital-logo.png" alt="Hospital logo">
        </template>

        <vs-tooltip right>
          <vs-sidebar-item>
              <template #icon>
                <box-icon name='home' ></box-icon>
              </template>

              <router-link to="/">Home</router-link>
          </vs-sidebar-item>

          <template #tooltip>
            Home
          </template>
        </vs-tooltip>

        <vs-tooltip right>
          <vs-sidebar-item>
              <template #icon>
                <box-icon name='user' ></box-icon>
              </template>

              <router-link to="/patient-detail">My profile</router-link>
          </vs-sidebar-item>

          <template #tooltip>
            My Profile
          </template>
        </vs-tooltip>

        <vs-sidebar-group>
          <template #header>
                <vs-sidebar-item arrow>
                    For patient
                </vs-sidebar-item>
            </template>

          <vs-sidebar-item>
              <template #icon>
                <box-icon type='solid' name='virus' ></box-icon>
              </template>

              <router-link to="/my-health-concerns">My health concerns</router-link>
          </vs-sidebar-item>
        </vs-sidebar-group>
        
        <vs-sidebar-group>
            <template #header>
                <vs-sidebar-item arrow>
                    For doctor
                </vs-sidebar-item>
            </template>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon type='solid' name='face-mask' ></box-icon>
                  </template>

                  <router-link to="/patients">Patients</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                My Profile
              </template>
            </vs-tooltip>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='user-plus'/>
                  </template>

                  <router-link to="/patient-add">Add new patient</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                  Add new patient
              </template>
            </vs-tooltip>

            <vs-tooltip right>
                <vs-sidebar-item>
                    <template #icon>
                      <box-icon type='solid' name='virus'/>
                    </template>

                    <router-link to="/health-concerns">Health concerns</router-link>
                </vs-sidebar-item>

                <template #tooltip>
                    Health concerns
                </template>
            </vs-tooltip>

            <vs-tooltip right>
                  <vs-sidebar-item>
                      <template #icon>
                        <box-icon name='blanket'></box-icon>
                      </template>

                      <router-link to="/assigned-tickets">Assigned tickets</router-link>
                  </vs-sidebar-item>

                  <template #tooltip>
                      Assigned tickets
                  </template>
            </vs-tooltip>
        </vs-sidebar-group>

        <vs-sidebar-group>
            <template #header>
                <vs-sidebar-item arrow>
                    For insurance worker
                </vs-sidebar-item>
            </template>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='list-plus' ></box-icon>
                  </template>

                  <router-link to="/examination-action-add">Add new Examination action</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                  Add new Examination action
              </template>
            </vs-tooltip>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='list-ul' ></box-icon>
                  </template>

                  <router-link to="/examination-actions-overview">Examination actions overview</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                  Examination actions overview
              </template>
            </vs-tooltip>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='money' ></box-icon>
                  </template>

                  <router-link to="/manage-requests">Manage payment requests</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                  Manage payment requests
              </template>
            </vs-tooltip>
        </vs-sidebar-group>

        <vs-sidebar-group>
            <template #header>
                <vs-sidebar-item arrow>
                    For admin
                </vs-sidebar-item>
            </template>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='user-detail' type='solid' ></box-icon>
                  </template>

                  <router-link to="/users-overview">Manage users</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                    Manage users
              </template>
            </vs-tooltip>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='user-plus'/>
                  </template>

                  <router-link to="/patient-add">Add new patient</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                  Add new patient
              </template>
            </vs-tooltip>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='plus-medical' type='solid' ></box-icon>
                  </template>

                  <router-link to="/doctor-add">Add new doctor</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                    Add new doctor
              </template>
            </vs-tooltip>

            <vs-tooltip right>
              <vs-sidebar-item>
                  <template #icon>
                    <box-icon name='user-plus' type='solid' ></box-icon>
                  </template>

                  <router-link to="/healthcare-worker-add">Add new healthcare worker</router-link>
              </vs-sidebar-item>

              <template #tooltip>
                    Add new healthcare worker
              </template>
            </vs-tooltip>
        </vs-sidebar-group>

        <template #footer v-on:click="redirectToProfile()">
            <div class="footer">
              <vs-card type="5">
                  <template #title>
                      <h3>Name and Surname</h3>
                  </template>

                  <template #img>
                      <img src="./assets/user-illu.jpg" alt="" width="200" height="200">
                  </template>

                  <template #text>
                    <p>
                      Logged as [Patient | Doc | Admin | HC]
                    </p>
                  </template>

                  <template #interactions>
                      <vs-tooltip>
                          <vs-button>
                              <box-icon name='comment-edit' animation='tada-hover' style="fill: #fbfbfb;"></box-icon>
                          </vs-button>

                          <template #tooltip>
                              Edit profile
                          </template>
                      </vs-tooltip>
                  </template>
              </vs-card>
            </div>
        </template>
      </vs-sidebar>
    </div>

    <div class="content">
      <router-view />
    </div>
  </div>
</template>

<script>
export default {
  name: 'App',

  components: {
  },

  data:() => ({
    active: 'home',
  }),

  methods: {
    redirectToProfile() {
      // Vue.$router.push({ name: 'patientDetail' });
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css?family=Roboto+Condensed');
@import url('https://fonts.googleapis.com/icon?family=Material+Icons');

html, body {
  font-family: 'Roboto', sans-serif;
  background-color: #fafafa !important;
}

.hidden {
    position: fixed;
}

box-icon {
  fill: #195bff;
}

.content {
  max-height: 100vh;
  background-color: #fafafa !important;
}

#app {
  background-color: #fff;
  font-family: 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}

@media only screen and (max-width: 600px) {
  .footer {
      display: none;
  }
}
</style>
