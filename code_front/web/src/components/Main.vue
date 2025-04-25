<template>
    <div>
      <div>
        <MenuBar class="menu-bar"></MenuBar>
      </div>
      <router-view class="router-view"></router-view>
    </div>
  </template>

  <script>
  import MenuBar from "./MenuBar";
  
  export default {
    name: "Main",
    components: {
      MenuBar
    },
    data() {
      return {}
    },
    mounted(){
      this.$router.push({
        name: "project_info"
      })
    },
    methods: {
      
    }
  }
  </script>

<style scoped>
.menu-bar{
  height: 2%;
  width: 100%;
}

.router-view{
  height: 98%;
  width: 100%;
}
</style>
  