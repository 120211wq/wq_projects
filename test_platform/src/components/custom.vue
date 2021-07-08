<template>
  <p v-for='(item,index) in table.value["01"]' :key="index">
    <span >{{ index }}</span>
    <el-input v-model="item[0]" ></el-input>
  </p>
<!--<p v-for='(item,index) in list' :key="index">{{item}}:{{index}}</p>-->
<!--  <p v-for='(item,index) in listObj' :key="index">{{item}}:{{index}}</p>-->
</template>

<script>
export default {
  name: "custom",
  created() {
    window.console.log('我进来了')
    window.console.log(this.$route.params.protocol_num)
  },
  data() {
    return {
      table: {
        "ident": 26420,
        "type": "plc_data",
        "value": {
          "code": "15638",
          "01": {
            "D压力": [
              1.1
            ],
            "三相电压A": [
              2
            ],
            "三相电压B": [
              3
            ],
            "三相电压C": [
              4
            ],
            "读表器": [
              5
            ],
            "耗电量": [
              6
            ],
            "冷凝出水温度": [
              7
            ],
            "三相电流B": [
              8
            ],
            "冷凝进水温度": [
              20
            ],
            "风机震动1": [
              9
            ]
          },
          "02": {
            "三相电流A": [
              10
            ],
            "锅炉故障1": [
              1, 3
            ]
          }
        },
        "flag": 3,
        "custom_type": "02"
      },
      input: '',
      list: [1, 2, 3, 4, 5, 6],
      listObj: {id: 1, name: 'zs1'},

    }
  },
  methods: {}
}
</script>

<style scoped>

</style>
