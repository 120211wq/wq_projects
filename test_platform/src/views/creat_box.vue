<template>
  <div style="text-align: left;margin-bottom: 20px">
    <el-radio-group v-model="formInline.box_type">
      <el-radio v-for="item in authTypeList"
                :key="item.id" :label="item.type" @change="agreeChange">
        {{ item.value }}
      </el-radio>
    </el-radio-group>
    <el-select v-model="formInline.protocol_num" placeholder="请选择" style="margin-left: 20px" v-show = see
    >
      <el-option
          v-for="item in options"
          :key="item.name"
          :label="item.name"
          :value="item.code">
      </el-option>
    </el-select>
  </div>
  <el-form :model="formInline" inline="true" :rules="rules" ref="formInline" label-width="100px" class="demo-ruleForm"
           style="text-align: left;">
    <el-radio-group v-model="formInline.env">
      <el-radio-button label="TEST">测试</el-radio-button>
      <el-radio-button label="DEV">生产</el-radio-button>
    </el-radio-group>
    <el-form-item label="奇享盒编码" prop="box_num">
      <el-input v-model="formInline.box_num" placeholder="请输入奇享盒编码"></el-input>
    </el-form-item>
    <el-form-item>
      <el-button type="primary" @click="submitForm('formInline')">模拟</el-button>
      <el-button @click="resetForm('formInline')">重置</el-button>
    </el-form-item>
  </el-form>

</template>

<script>
/* eslint-disable */
import axios from "axios";
import {defineComponent, h} from 'vue'
import {ElMessage} from 'element-plus'
import {get_simulationlist, getProtocolList, submit_createBox} from '../api/index'

export default {
  created() {
    this.get_sel_list();
  },
  data() {
    return {
      see:false,
      options: [],
      AuthoCheck: 1,
      authTypeList: [{id: 1, value: '蒸汽锅炉', type: 1}, {id: 2, value: '热水锅炉', type: 2}, {
        id: 3,
        value: '自定义协议',
        type: 3
      }],
      radio1: 'TEST',
      formInline: {
        box_num: '',
        env: 'TEST',
        box_type: 1,
        protocol_num : 2
      },
      rules: {
        box_num: [{required: true, message: '请输入奇享盒编码', trigger: 'blur'}]
      }
    }
  },
  methods: {
    get_sel_list() {
      getProtocolList()
          .then(res => {
            if (res.status === 200){
              this.options = res.data.result;
            }

          });
    },
    agreeChange() {
      if (this.formInline.box_type === 3) {
        window.console.log("选到3了")
        this.see = true
      }
      else if(this.formInline.box_type === 2){
        this.see = false
        this.formInline.protocol_num = 20001
        window.console.log(this.formInline.protocol_num)
      }
      else {
        this.see = false
        this.formInline.protocol_num = 10001
        window.console.log(this.formInline.protocol_num)

      }
    },
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          var that = this;
          submit_createBox(that.formInline)
              .then(res => {
                window.console.log(res.status)
                if (res.status === 200) {
                  console.log(res);
                  ElMessage.success(res.data.state);
                }
              });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
    // },
    // watch: {
    //   radio1(val) {
    //     console.log(val)
    //   }
  }
}
/* eslint-disable */
</script>
<style>
.el-row1 {
  padding-right: 0;
}
</style>

