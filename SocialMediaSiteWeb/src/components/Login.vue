<template>
    <div>
        <el-input placeholder="请输入用户名" prefix-icon="el-icon-user" v-model="username"></el-input>
        <el-input placeholder="请输入密码" prefix-icon="el-icon-lock" v-model="password" show-password></el-input>

        <el-button type="primary">登陆</el-button>
        <el-button type="primary">注册</el-button>
    </div>
</template>

<script>
import { Vue } from 'vue-property-decorator';

export default {
  name: 'login',
  components: {

  },
  data: {
      username: '',
      password: '',
  }
};
</script>

<style scoped>

</style>