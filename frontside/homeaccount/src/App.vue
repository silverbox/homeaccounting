<template>
  <div id="app">
    <el-menu
      :default-active="activeIndex"
      class="el-menu-navi"
      mode="horizontal"
      @select="handleNavSelect">
      <router-link tag="el-menu-item" id="el-menu-nav" to="/input" index="1">Input</router-link>
      <router-link tag="el-menu-item" id="el-menu-nav" to="/list" index="2">List</router-link>
      <router-link tag="el-menu-item" id="el-menu-nav" to="/graph" index="3">Graph</router-link>
      <router-link tag="el-menu-item" id="el-menu-nav" to="/table" index="4">Table</router-link>
    </el-menu>
  <!--
    <el-tabs v-model="activeName" @tab-click="handleTabClick">
      <el-tab-pane label="Input" name="input">Input</el-tab-pane>
      <el-tab-pane label="List" name="list">List</el-tab-pane>
      <el-tab-pane label="Graph" name="graph">Graph</el-tab-pane>
      <el-tab-pane label="Table" name="table">Table</el-tab-pane>
    </el-tabs>
  <img src="./assets/logo.png">
   -->
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      activeIndex: '1'
    }
  },
  methods: {
    handleNavSelect (tab, event) {
      console.log(tab, event)
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 10px;
}
</style>
