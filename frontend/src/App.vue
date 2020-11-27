<template>
  <div id="app">
    <div v-if="this.$route.path !== '/'">
      <vs-sidebar
      v-model="active"
      :open="windowWidth >= 1200 || (windowWidth < 1200 && activeSidebar)"
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

              <router-link
                  v-if="userRole === 'healthcare-worker'"
                  :to="`/profile/health-insurance-worker/${user.id}`"
              >
                My profile
              </router-link>

              <router-link
                  v-else
                  :to="`/profile/${userRole}/${user.id}`"
              >
                My profile
              </router-link>
          </vs-sidebar-item>

          <template #tooltip>
            My Profile
          </template>
        </vs-tooltip>

        <vs-sidebar-group v-if="userRole === 'patient' || userRole === 'admin'">
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
        
        <vs-sidebar-group v-if="userRole === 'doctor' || userRole === 'admin'">
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

        <vs-sidebar-group v-if="userRole === 'healthcare-worker' || userRole === 'admin'">
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

        <vs-sidebar-group v-if="userRole === 'admin'">
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

        <template #footer>
            <div class="footer" >
              <vs-card type="5">
                  <template #title>
                      <h3>{{ user.first_name }} {{ user.last_name }}</h3>
                  </template>

                  <template #img>
                      <img src="./assets/user-illu.jpg" alt="" width="200" height="200">
                  </template>

                  <template #text>
                    <p>
                      Logged as {{ userRole.replace('-', ' ') }}
                    </p>
                  </template>

                  <template #interactions>
                      <vs-tooltip>
                          <vs-button @click="logout" danger>
                                <box-icon name='log-out' animation='tada-hover' style="fill: #fbfbfb;"/>
                          </vs-button>

                          <template #tooltip>
                              Logout
                          </template>
                      </vs-tooltip>
                    
                      <vs-tooltip>
                          <vs-button @click="editUserProfile(user.id, userRole)">
                              <box-icon name='comment-edit' animation='tada-hover' style="fill: #fbfbfb;"/>
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
      <div class="expand__sidebar">
        <vs-button
            v-if="windowWidth < 1200"
            @click="activeSidebar = !activeSidebar"
            flat
            icon
        >
              <box-icon name='menu'/>
        </vs-button>
      </div>

      <div @click="hideSideBar()">
          <router-view />
      </div>
    </div>

    <vs-dialog
        width="600px"
        v-model="activeLogout"
    >
        <template #header>
        <h5>
            Are you sure you want to log out?
        </h5>
        </template>

        <template #footer>
            <img src="./assets/logout.svg" alt="" width="400">

            <div class="center">
                <vs-button
                    @click="logoutConfirm()"
                    danger
                >
                    Yep, leave
                </vs-button>

                <vs-button
                    @click="abortLeaving()"
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
import { useWindowSize } from 'vue-window-size';
import { store } from '@/store/store';
import { mapState } from 'vuex';

export default {
  name: 'App',

  components: {
  },

  data:() => ({
    active: 'home',
    activeSidebar: false,
    store_copy: store,
    activeLogout: false,
  }),

  setup() {
    const { width, height } = useWindowSize();
    return {
      windowWidth: width,
      windowHeight: height,
    };
  },

  computed: {
    ...mapState([
        'user',
        'userRole',
    ])
  },

  methods: {
      showUserProfile(userId, role) {
          this.$router.push({ name: 'profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }})
      },

      editUserProfile(userId, role) {
          this.$router.push({ name: 'edit-profile', params: {id: userId, role: role.replace(/ /g, '-').toLowerCase() }})
      },

      hideSideBar() {
          if (this.activeSidebar === true) {
              this.activeSidebar = !this.activeSidebar;
          } else {
              this.activeSidebar = false;
          }
      },

      logout() {
          this.activeLogout = true;
      },

      abortLeaving() {
          this.activeLogout = false;
      },

      logoutConfirm() {
        this.activeLogout = false;
        this.$store.dispatch('logoutUser')
            .then(() => {
              this.$router.push('/');
              this.window.sessionStorage.clear();
            })
      },
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

.expand__sidebar {
  margin-left: 1em;
  margin-top: 1em;
}

.center {
  float: right;
  padding-top: 12em;
  margin-bottom: 3em;
}

@media only screen and (max-width: 600px) {
  .footer {
      display: none;
  }
}
</style>
