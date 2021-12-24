<template>
  <el-row>
    <el-page-header @back="toURL1" content="详情页面">
    </el-page-header>
    <el-col>
      <p style="text-align:left">盒子编号：{{ box_number }}</p>
      <p style="text-align:left ">盒子类型：{{ box_type_list[box_type] }}</p>
    </el-col>
  </el-row>
  <el-tabs v-model="activeName" @tab-click="handleClick">
    <el-tab-pane label="plc数据" name="first">
      <el-form :model="plcForm" :rules="plc_rules" ref="plcForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="炉水温度" prop="plc1">
          <el-input v-model="plcForm.plc1"
                    oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{3,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"
          ></el-input>
        </el-form-item>
        <el-form-item label="出水温度" prop="plc2">
          <el-input v-model="plcForm.plc2" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="回水温度" prop="plc3">
          <el-input v-model="plcForm.plc3" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="烟道温度" prop="plc4">
          <el-input v-model="plcForm.plc4" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="节能器烟温" prop="plc5">
          <el-input v-model="plcForm.plc5" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="冷凝出口烟温" prop="plc6">
          <el-input v-model="plcForm.plc6" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="冷凝出水温度" prop="plc7">
          <el-input v-model="plcForm.plc7" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item style="margin-left: 0">
          <el-switch
              @change="continuous_plc"
              v-model="plc_switch"
              inactive-text="持续上报"
              active-color="#13ce66"
              inactive-color="#ff4949"
              style="float: left">
          </el-switch>
          <el-button type="primary" @click="submitplc('plcForm')">立即上报</el-button>
          <el-button @click="resetForm('plcForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
    <el-tab-pane label="电量数据" name="second">
      <el-form :model="powerForm" :rules="power_rules" ref="powerForm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="A 相电压" prop="power1">
          <el-input v-model="powerForm.power1" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="B 相电压" prop="power2">
          <el-input v-model="powerForm.power2" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="C 相电压" prop="power3">
          <el-input v-model="powerForm.power3" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="A 相电流" prop="power4">
          <el-input v-model="powerForm.power4" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="B 相电流" prop="power5">
          <el-input v-model="powerForm.power5" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="C 相电流" prop="power6">
          <el-input v-model="powerForm.power6" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="功率" prop="power7">
          <el-input v-model="powerForm.power7" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="功率因子" prop="power8">
          <el-input v-model="powerForm.power8" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item label="能量" prop="power9">
          <el-input v-model="powerForm.power9" oninput="value=value.replace(/[^\d.]/g, '').replace(/\.{2,}/g, '.').replace('.', '$#$').replace(/\./g, '').
                    replace('$#$', '.').replace(/^(\-)*(\d+)\.(\d).*$/, '$1$2.$3').replace(/^\./g, '')"></el-input>
        </el-form-item>
        <el-form-item>
          <el-switch
              @change="continuous_power"
              v-model="power_switch"
              inactive-text="持续上报"
              active-color="#13ce66"
              inactive-color="#ff4949"
              style="float: left">
          </el-switch>
          <el-button type="primary" @click="submitpower('powerForm')">立即上报</el-button>
          <el-button @click="resetForm('powerForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
    <el-tab-pane label="告警数据" name="third">
      <el-form :model="alarm" label-width="100px" class="demo-ruleForm">
        <el-form-item label="锅炉运行状态">
          <el-radio v-model="alarm.alarm1" label='0'>锅炉停止</el-radio>
          <el-radio v-model="alarm.alarm1" label='1'>锅炉小火</el-radio>
          <el-radio v-model="alarm.alarm1" label='2'>锅炉大火</el-radio>
        </el-form-item>
        <el-form-item label="热水锅炉故障-1">
          <el-checkbox-group v-model=alarm.checkList1>
            <el-checkbox label='1'>本体烟温超高</el-checkbox>
            <el-checkbox label=2>循环水流故障</el-checkbox>
            <el-checkbox label=4>定时关机</el-checkbox>
            <el-checkbox label=5>炉水超温故障</el-checkbox>
            <el-checkbox label=6>冷凝出口烟温传感器故障</el-checkbox>
            <el-checkbox label=8>冷凝出水温度传感器故障</el-checkbox>
            <el-checkbox label=9>回水温度传感器故障</el-checkbox>
            <el-checkbox label=10>出水温度传感器故障</el-checkbox>
            <el-checkbox label=11>本体烟温传感器故障</el-checkbox>
            <el-checkbox label=12>水位极低</el-checkbox>
            <el-checkbox label=13>燃烧机故障</el-checkbox>
            <el-checkbox label=14>出水超温</el-checkbox>
            <el-checkbox label=15>出水压力极低</el-checkbox>
            <el-checkbox label=16>出水压力极高</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="热水锅炉故障-1">
          <el-checkbox-group v-model=alarm.checkList2>
            <el-checkbox label='1'>炉内压力极高</el-checkbox>
            <el-checkbox label=2>真空泵故障</el-checkbox>
            <el-checkbox label=3>炉水温度传感器故障</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitalarm">立即上报</el-button>
        </el-form-item>
      </el-form>
    </el-tab-pane>
  </el-tabs>
</template>

<script>
/* eslint-disable */

import axios from "axios";
import {ElMessage} from 'element-plus'
import {simulation} from '../api/index'
import {stop_continuous} from '../api/index'
import {start_continuous} from '../api/index'


/* eslint-disable */
export default {
  mounted() {

  },
  data() {
    return {
      box_type_list:{
        1:'蒸汽锅炉',
        2:'热水锅炉'
      },
      plc_switch: false,
      power_switch: false,
      params: {
        type: '(1,2,3)'
      },
      activeName: 'second',
      plcForm:
          {
            plc1: 90,
            plc2: 82,
            plc3: 50,
            plc4: 24,
            plc5: 56,
            plc6: 122,
            plc7: 99
          },
      plc_rules: {
        plc1: [{required: true, message: '必填'}],
        plc2: [{required: true, message: '必填'}],
        plc3: [{required: true, message: '必填'}],
        plc4: [{required: true, message: '必填'}],
        plc5: [{required: true, message: '必填'}],
        plc6: [{required: true, message: '必填'}],
        plc7: [{required: true, message: '必填'}]
      },
      powerForm:
          {
            power1: 213.3,
            power2: 218.5,
            power3: 211.4,
            power4: 12.2,
            power5: 12.0,
            power6: 11.6,
            power7: 6.9,
            power8: 0.90,
            power9: 18706.1
          },
      alarm: {
        alarm1: '1',
        checkList1: ['1'],
        checkList2: ['1']
      },
      power_rules: {
        power1: [{required: true, message: '必填'}],
        power2: [{required: true, message: '必填'}],
        power3: [{required: true, message: '必填'}],
        power4: [{required: true, message: '必填'}],
        power5: [{required: true, message: '必填'}],
        power6: [{required: true, message: '必填'}],
        power7: [{required: true, message: '必填'}],
        power8: [{required: true, message: '必填'}],
        power9: [{required: true, message: '必填'}]
      }
    };
  },
  methods: {
    continuous_power() {
      if (this.power_switch === true) {
        const continuous_power_body = {
          ident: Number(this.thread_ident),
          type: 'ele_data',
          value: [[Number(this.powerForm.power1) * 10, Number(this.powerForm.power2) * 10, Number(this.powerForm.power3) * 10, Number(this.powerForm.power4) * 10,
            Number(this.powerForm.power5) * 10, Number(this.powerForm.power6) * 10, Number(this.powerForm.power7) * 100, Number(this.powerForm.power8) * 10], Number(this.powerForm.power9) * 10]
          ,
          flag: 2
        }
        start_continuous(continuous_power_body)
            .then(res => {
              ElMessage.success('开启电量持续上报')
              this.ele_con_ident = res.data.ident[0][0];
            });
      } else {
        window.console.log('我关闭持续上报啦');
        const stop_continuous_body = {box_id: this.box_number, stop_ident: this.ele_con_ident, type: 'ele_data'}
        stop_continuous(stop_continuous_body).then(res => {
          if(res.data.status === 200){
            ElMessage.success('停止持续上报成功')
            this.power_switch = false
          }
          else {
            ElMessage.success('停止持续上报失败')
          }
        });
      }
    },
    continuous_plc() {
      if (this.plc_switch === true) {
        const continuous_plc_body = {
          ident: Number(this.thread_ident),
          type: 'plc_data',
          value: [Number(this.plcForm.plc1) * 10, Number(this.plcForm.plc2) * 10, Number(this.plcForm.plc3) * 10, Number(this.plcForm.plc4) * 10,
            Number(this.plcForm.plc5) * 10, Number(this.plcForm.plc6) * 10, Number(this.plcForm.plc7) * 10],
          flag: 2
        }
        start_continuous(continuous_plc_body)
            .then(res => {
              ElMessage.success('开启plc持续上报')
              this.plc_con_ident = res.data.ident[0][0];
            });
      } else {
        window.console.log('我关闭持续上报啦');
        const stop_continuous_body = {box_id: this.box_number, stop_ident: this.plc_con_ident, type: 'plc_data'}
        stop_continuous(stop_continuous_body).then(res => {
          if(res.data.status === 200){
            ElMessage.success('停止持续上报成功')
            this.plc_switch = false
          }
          else {
            ElMessage.success('停止持续上报失败')
          }
        });
      }
    },
    submitalarm() {
      const sub_alarm_body = {
        ident: Number(this.thread_ident),
        type: 'plc_state',
        value: [[Number(this.alarm.alarm1)], this.alarm.checkList1.map(Number), this.alarm.checkList2.map(Number)],
        flag: 1
      }
      simulation(sub_alarm_body)
          .then(res => {
            console.log(res);
          });
    },
    toURL1() {
      this.$router.push({name: 'box_list'})
    },
    handleClick(tab, event) {
      console.log(tab, event);
    },
    submitplc(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const sub_plc_body = {
            ident: Number(this.thread_ident),
            type: 'plc_data',
            value: [Number(this.plcForm.plc1) * 10, Number(this.plcForm.plc2) * 10, Number(this.plcForm.plc3) * 10, Number(this.plcForm.plc4) * 10,
              Number(this.plcForm.plc5) * 10, Number(this.plcForm.plc6) * 10, Number(this.plcForm.plc7) * 10],
            flag: 1
          }
          simulation(sub_plc_body)
              .then(res => {
                console.log(res);
              });
        } else {
          console.log('error submit!!');
          return false;
        }
      });
    },
    submitpower(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const sub_power_body = {
            ident: Number(this.thread_ident),
            type: 'ele_data',
            value: [[Number(this.powerForm.power1) * 10, Number(this.powerForm.power2) * 10, Number(this.powerForm.power3) * 10, Number(this.powerForm.power4) * 10,
              Number(this.powerForm.power5) * 10, Number(this.powerForm.power6) * 10, Number(this.powerForm.power7) * 100, Number(this.powerForm.power8) * 10], Number(this.powerForm.power9) * 10]
            ,
            flag: 1
          }
          simulation(sub_power_body)
              .then(res => {
                console.log(res);
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
  },
  created() {
    var _this = this
    _this.box_number = this.$route.params.box_number
    _this.thread_ident = this.$route.params.thread_ident
    _this.ele_con_ident = this.$route.params.ele_con_ident
    _this.plc_con_ident = this.$route.params.plc_con_ident
    _this.box_type = this.$route.params.box_type
    if(_this.ele_con_ident !== 'null'){
      _this.power_switch = true
    }
    if(_this.plc_con_ident !== 'null'){
      _this.plc_switch = true
    }
  }
}


</script>

<style scoped>

</style>
