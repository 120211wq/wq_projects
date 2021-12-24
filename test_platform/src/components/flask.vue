
<!--<template>-->
<!--  <div id='vue'>-->
<!--    <el-switch-->
<!--  v-model="value1"-->
<!--  active-text="按月付费" active-value=1 inactive-value=2 active-color=#409EFE  @change="getData2">-->
<!--</el-switch>-->
<!--<el-switch-->
<!--  style="display: block"-->
<!--  v-model="value2"-->
<!--  active-color="#13ce66"-->
<!--  inactive-color="#ff4949"-->
<!--  active-text="按月付费"-->
<!--  inactive-text="按年付费">-->
<!--</el-switch>-->
<!--    <el-breadcrumb separator-class="el-icon-arrow-right">-->
<!--    <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>-->
<!--    <el-breadcrumb-item :to="{ path: '/flask' }" >活动管理</el-breadcrumb-item>-->
<!--    <el-breadcrumb-item :to="{ path: '/' }">活动列表</el-breadcrumb-item>-->
<!--    <el-breadcrumb-item>活动详情</el-breadcrumb-item>-->
<!--    </el-breadcrumb>-->
<!--    <button @click="getData1">GET DATA1</button>-->
<!--    <el-table-->
<!--    :data="tableData"-->
<!--    stripe-->
<!--    style="width: 100%">-->
<!--    <el-table-column-->
<!--      prop="date"-->
<!--      label="日期"-->
<!--      width="180">-->
<!--    </el-table-column>-->
<!--    <el-table-column-->
<!--      prop="name"-->
<!--      label="姓名"-->
<!--      width="180">-->
<!--    </el-table-column>-->
<!--    <el-table-column-->
<!--      prop="address"-->
<!--      label="地址">-->
<!--    </el-table-column>-->
<!--  </el-table>-->
<!--  <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="100px" class="demo-ruleForm">-->
<!--  <el-form-item label="活动名称" prop="name">-->
<!--    <el-input v-model="ruleForm.name"></el-input>-->
<!--  </el-form-item>-->
<!--  <el-form-item label="活动区域" prop="region">-->
<!--    <el-select v-model="ruleForm.region" placeholder="请选择活动区域">-->
<!--      <el-option label="区域一" value="shanghai"></el-option>-->
<!--      <el-option label="区域二" value="beijing"></el-option>-->
<!--    </el-select>-->
<!--  </el-form-item>-->
<!--  <el-form-item label="活动时间" required>-->
<!--    <el-col :span="11">-->
<!--      <el-form-item prop="date1">-->
<!--        <el-date-picker type="date" placeholder="选择日期" v-model="ruleForm.date1" style="width: 100%;"></el-date-picker>-->
<!--      </el-form-item>-->
<!--    </el-col>-->
<!--    <el-col class="line" :span="2">-</el-col>-->
<!--    <el-col :span="11">-->
<!--      <el-form-item prop="date2">-->
<!--        <el-time-picker placeholder="选择时间" v-model="ruleForm.date2" style="width: 100%;"></el-time-picker>-->
<!--      </el-form-item>-->
<!--    </el-col>-->
<!--  </el-form-item>-->
<!--  <el-form-item label="即时配送" prop="delivery">-->
<!--    <el-switch v-model="ruleForm.delivery"></el-switch>-->
<!--  </el-form-item>-->
<!--  <el-form-item label="活动性质" prop="type">-->
<!--    <el-checkbox-group v-model="ruleForm.type">-->
<!--      <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>-->
<!--      <el-checkbox label="地推活动" name="type"></el-checkbox>-->
<!--      <el-checkbox label="线下主题活动" name="type"></el-checkbox>-->
<!--      <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>-->
<!--    </el-checkbox-group>-->
<!--  </el-form-item>-->
<!--  <el-form-item label="特殊资源" prop="resource">-->
<!--    <el-radio-group v-model="ruleForm.resource">-->
<!--      <el-radio label="线上品牌商赞助"></el-radio>-->
<!--      <el-radio label="线下场地免费"></el-radio>-->
<!--    </el-radio-group>-->
<!--  </el-form-item>-->
<!--  <el-form-item label="活动形式" prop="desc">-->
<!--    <el-input type="textarea" v-model="ruleForm.desc"></el-input>-->
<!--  </el-form-item>-->
<!--  <el-form-item>-->
<!--    <el-button type="primary" @click="submitForm('ruleForm')">立即创建</el-button>-->
<!--    <el-button @click="resetForm('ruleForm')">重置</el-button>-->
<!--  </el-form-item>-->
<!--</el-form>-->
<!--  <el-input v-model="input" placeholder="请输入内容"></el-input>-->
<!--  <div id="chartPie" class="pie-wrap"></div>-->
<!--  </div>-->

<!--</template>-->

<!--<script>-->
<!--/* eslint-disable */-->
<!--import axios from "axios";-->
<!--import test1 from './creat_box.vue'-->

<!--export default {-->
<!--  components: {test1},-->
<!--  data: function() {-->
<!--    return {-->
<!--      value1: true,-->
<!--      value2: true,-->
<!--      serverResponse: "resp",-->
<!--      input: '',-->
<!--      ruleForm: {-->
<!--          name: '',-->
<!--          region: '',-->
<!--          date1: '',-->
<!--          date2: '',-->
<!--          delivery: false,-->
<!--          type: [],-->
<!--          resource: '',-->
<!--          desc: ''-->
<!--        },rules: {-->
<!--          name: [-->
<!--            { required: true, message: '请输入活动名称', trigger: 'blur' },-->
<!--            { min: 3, max: 5, message: '长度在 3 到 5 个字符', trigger: 'blur' }-->
<!--          ],-->
<!--          region: [-->
<!--            { required: true, message: '请选择活动区域', trigger: 'change' }-->
<!--          ],-->
<!--          date1: [-->
<!--            { type: 'date', required: true, message: '请选择日期', trigger: 'change' }-->
<!--          ],-->
<!--          date2: [-->
<!--            { type: 'date', required: true, message: '请选择时间', trigger: 'change' }-->
<!--          ],-->
<!--          type: [-->
<!--            { type: 'array', required: true, message: '请至少选择一个活动性质', trigger: 'change' }-->
<!--          ],-->
<!--          resource: [-->
<!--            { required: true, message: '请选择活动资源', trigger: 'change' }-->
<!--          ],-->
<!--          desc: [-->
<!--            { required: true, message: '请填写活动形式', trigger: 'blur' }-->
<!--          ]-->
<!--        },-->
<!--      tableData: [{-->
<!--            'date': '2016-05-02',-->
<!--            'name': '王小虎',-->
<!--            'address': '上海市普陀区金沙江路 1518 弄'-->
<!--          }]-->
<!--    };-->
<!--  },-->
  mounted() {
      this.get_tableData();
    },
<!--  methods: {-->
<!--    submitForm(formName) {-->
<!--        this.$refs[formName].validate((valid) => {-->
<!--          if (valid) {-->
<!--            alert('submit!');-->
<!--          } else {-->
<!--            console.log('error submit!!');-->
<!--            return false;-->
<!--          }-->
<!--        });-->
<!--      },-->
<!--      resetForm(formName) {-->
<!--        this.$refs[formName].resetFields();-->
<!--      },-->
<!--    get_tableData() {-->
<!--      var that = this;-->
<!--      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address-->
<!--      const path = "http://127.0.0.1:5000/get_tableData";-->
<!--      axios-->
<!--        .get(path)-->
<!--        .then(function(response) {-->
<!--          // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串-->
<!--          // 可以直接通过 response.data 取key-value-->
<!--          // 坑一：这里不能直接使用 this 指针，不然找不到对象-->
<!--          window.console.log(response)-->
<!--          // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串-->
<!--          that.tableData = response.data.tableData;-->
<!--          window.console.log(that.tableData)-->

<!--        })-->
<!--        .catch(function(error) {-->
<!--          alert("Error " + error);-->
<!--        });-->
<!--    },-->
<!--    getData1() {-->
<!--      var that = this;-->
<!--      // 对应 Python 提供的接口，这里的地址填写下面服务器运行的地址，本地则为127.0.0.1，外网则为 your_ip_address-->
<!--      const path1 = "http://127.0.0.1:5000/getname";-->
<!--      axios-->
<!--        .get(path1)-->
<!--        .then(function(response) {-->
<!--          // 这里服务器返回的 response 为一个 json object，可通过如下方法需要转成 json 字符串-->
<!--          // 可以直接通过 response.data 取key-value-->
<!--          // 坑一：这里不能直接使用 this 指针，不然找不到对象-->
<!--          window.console.log(response)-->
<!--          var msg = response.data.name;-->
<!--          // 坑二：这里直接按类型解析，若再通过 JSON.stringify(msg) 转，会得到带双引号的字串-->
<!--          that.serverResponse = msg;-->

<!--          alert(-->
<!--            "Success " + response.status + ", " + response.data + ", " + msg-->
<!--          );-->
<!--        })-->
<!--        .catch(function(error) {-->
<!--          alert("Error " + error);-->
<!--        });-->
<!--    },-->
<!--     getData2() {-->
<!--      // var that = this;-->
<!--      var test1 = this.value1;-->
<!--      window.console.log(test1)-->
<!--      }-->
<!--  },-->
<!--};-->
<!--/* eslint-disable */-->
<!--</script>-->
