<template>
  <RouterView></RouterView>
  <el-table
      :data="tableData"
      v-loading="loading"
      style="width: 100%">
    <el-table-column
        prop="record_time"
        label="模拟时间"
        width="180">
    </el-table-column>
    <el-table-column
        prop="box_number"
        label="盒子编号"
        width="180">
    </el-table-column>
    <el-table-column
        prop="env"
        label="环境"
        width="120">
      <template v-slot="scope">
        <span v-if="scope.row.env === 'TEST'">测试环境</span>
        <span v-if="scope.row.env === 'DEV'">开发环境</span>
      </template>
    </el-table-column>

    <el-table-column
        prop="box_type"
        label="盒子类型"
        width="120">
      <template v-slot="scope">
        <span v-if="scope.row.box_type === 1">蒸汽锅炉</span>
        <span v-if="scope.row.box_type === 2">热水锅炉</span>
      </template>
    </el-table-column>
    <el-table-column
        prop="box_count"
        label="盒子数量">
    </el-table-column>
    <el-table-column
        prop="thread_ident"
        label="进程号">
    </el-table-column>
    <el-table-column
        prop="runnning_type"
        label="当前模拟状态">
      <template v-slot="scope">
        <span v-if="scope.row.runnning_type === 1">正常</span>
        <span v-if="scope.row.runnning_type === 2">停止</span>
      </template>
    </el-table-column>
    <el-table-column
        fixed="right"
        label="操作"
    >
      <template #default="scope">
        <!--        <el-button @click="handleClick(scope.row)" type="primary" size="small">查看</el-button>-->
        <el-button @click="toURL((scope.row))" type="primary" size="small">查看</el-button>
        <el-button type="danger" size="small" @click="handlestop(scope.row)">停止模拟</el-button>
      </template>
    </el-table-column>
  </el-table>

</template>

<script>
/* eslint-disable */
import axios from "axios";
import {ElMessage} from 'element-plus'
import {get_simulationlist, simulation_stopBox} from "../api";

export default {
  created() {
    this.get_tableData();
  },

  methods: {
    open3(msg) {
      ElMessage.success({
        message: msg,
        type: 'success'
      });
    },
    open5(msg) {
      ElMessage.error(msg);
    },
    toURL(row) {
      if (row.box_type === 1) {
        window.console.log(row.box_type)
        this.$router.push({name: 'steam_simulation',
          params: {
            box_number: row.box_number,
            thread_ident: row.thread_ident,
            ele_con_ident: row.ele_con_ident,
            plc_con_ident: row.plc_con_ident,
            box_type: row.box_type
          }
        })
      } else {
        window.console.log(row.box_type)
        window.console.log(this.$router)
        this.$router.push({name: 'hot_water_simulation',
          params: {
            box_number: row.box_number,
            thread_ident: row.thread_ident,
            ele_con_ident: row.ele_con_ident,
            plc_con_ident: row.plc_con_ident,
            box_type: row.box_type
          }
        })
      }
    },
    handlestop(row) {
      var that = this;
      const stop_body2 = {ident: ''}
      stop_body2.ident = row.thread_ident.toString()
      simulation_stopBox(stop_body2)
          .then(res => {
            if (res.status === 200){
              console.log(res)
              ElMessage.success('停止成功')
            }
            
          });
      setTimeout(that.get_tableData, 1000);
    },
    get_tableData() {
      // var that = this;
      get_simulationlist(this.body1)
          .then(res => {
             if (res.status === 200){
               this.tableData = res.data.result;
              this.loading = false;
              console.log(res);
             }
            
          });
    }
  },
  data() {
    return {
      loading: true,
      tableData: [],
      id1: '',
      body1: {
        type: '(1,2,3)'
      },
    }
  }
}
/* eslint-disable */
</script>

<style>
.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}

body {
  margin: 0;
}
</style>
