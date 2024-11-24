<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import { request } from '@/service/request';
// import { fetchStockDataAndPrediction, fetchStockFinancialData } from '@/service/api/stock-detail';

const stockInfoData = ref([]);
const stockDetailData = ref([]);

const route = useRoute();
const router = useRouter();
const stockCode = route.query.stockCode;
console.log(stockCode);

// const routeQuery = computed(() => JSON.stringify(route.query));

async function fetchStockFinancialData(stockCode) {
  try {
    const result = await request({
      url: '/stock/financial_data',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        stockCode
      },
      method: 'GET'
    });
    if (result) {
      // console.log(result.data);
      stockInfoData.value = result.data; // 存储获取到的股票指数数据
    } else {
      // console.error('Error fetching stock indices:', result.message);
    }
  } catch (error) {
    // console.error('Error fetching stock indices:', error);
  }
}
async function fetchstockDetailData(stockCode) {
  try {
    const result = await request({
      url: '/stock',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        stockCode
      },
      method: 'GET'
    });
    if (result) {
      console.log(result.data);
      stockDetailData.value = result.data; // 存储获取到的股票指数数据
    } else {
      // console.error('Error fetching stock indices:', result.message);
    }
  } catch (error) {
    // console.error('Error fetching stock indices:', error);
  }
}

const stockDetail = ref({
  stockCode: '000821',
  stockName: '京山轻机',
  industry: null,
  latestPrice: '11.56',
  priceChangeRate: '2.76',
  priceChange: '0.31',
  riseSpeed: '0.09',
  ratingOrgNum: 9,
  ratingBuyNum: 7,
  ratingAddNum: 2,
  ratingNeutralNum: 0,
  ratingReduceNum: 0,
  ratingSaleNum: 0,
  year1: 2023,
  eps1: 0.540262,
  year2: 2024,
  eps2: 0.87375,
  year3: 2025,
  eps3: 1.11375,
  year4: 2026,
  eps4: 1.48125
});
const stockInfo = ref({
  stockCode: '000821',
  summary: '2023年前三季度归母净利润同比大增62.2%，约为2627万元',
  financialDataByYear: {
    '2018': {
      totalOperatereveIncrease: -19.974,
      parentNetprofitIncrease: -124.6,
      dnetprofitatpcTcalIncrease: -150.6
    },
    '2019': {
      totalOperatereveIncrease: 20.398,
      parentNetprofitIncrease: 127.1,
      dnetprofitatpcTcalIncrease: -9
    },
    '2020': {
      totalOperatereveIncrease: 14.624,
      parentNetprofitIncrease: 156.6,
      dnetprofitatpcTcalIncrease: -202.3
    },
    '2021': {
      totalOperatereveIncrease: 0.796,
      parentNetprofitIncrease: -1014.2,
      dnetprofitatpcTcalIncrease: -12.6
    },
    '2022': {
      totalOperatereveIncrease: -34.017,
      parentNetprofitIncrease: -175.4,
      dnetprofitatpcTcalIncrease: -178.4
    },
    '2023前三季度': {
      totalOperatereveIncrease: -25.979,
      parentNetprofitIncrease: -35.9,
      dnetprofitatpcTcalIncrease: -34
    }
  }
});
// 将字符串属性转换为数字并保留两位小数
stockDetail.value = {
  ...stockDetail.value,
  latestPrice: Math.round(Number.parseFloat(stockDetail.value.latestPrice) * 100) / 100,
  priceChangeRate: Math.round(Number.parseFloat(stockDetail.value.priceChangeRate) * 100) / 100,
  priceChange: Math.round(Number.parseFloat(stockDetail.value.priceChange) * 100) / 100,
  riseSpeed: Math.round(Number.parseFloat(stockDetail.value.riseSpeed) * 100) / 100
};
stockDetailData.value = {
  ...stockDetailData.value,
  latestPrice: Math.round(Number.parseFloat(stockDetailData.value.latestPrice) * 100) / 100,
  priceChangeRate: Math.round(Number.parseFloat(stockDetailData.value.priceChangeRate) * 100) / 100,
  priceChange: Math.round(Number.parseFloat(stockDetailData.value.priceChange) * 100) / 100
};

const goBack = () => {
  router.back();
};

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const pieChartConfig = {
  backgroundColor: 'transparent',
  series: [
    {
      type: 'pie',
      radius: '40%', // 缩小图表半径
      data: [
        { value: stockDetail.value.ratingBuyNum, name: '买进指数', itemStyle: { color: '#d62728' } }, // 红色
        { value: stockDetail.value.ratingAddNum, name: '增持指数', itemStyle: { color: '#ff7f0e' } }, // 橙色
        { value: stockDetail.value.ratingNeutralNum || 0, name: '观望指数', itemStyle: { color: '#2ca02c' } }, // 绿色
        { value: stockDetail.value.ratingReduceNum || 0, name: '减持指数', itemStyle: { color: '#9467bd' } }, // 紫色
        { value: stockDetail.value.ratingSaleNum || 0, name: '卖出指数', itemStyle: { color: '#1f77b4' } } // 蓝色
      ].filter(item => item.value > 0), // 过滤掉值为0的数据
      label: {
        fontSize: 10, // 缩小字体
        formatter(params) {
          return `${params.name}: ${params.value}`;
        }
      },
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
};

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    chartInstance.setOption(pieChartConfig);
    fetchStockFinancialData(stockCode);
    fetchstockDetailData(stockCode);
  }
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
});
const barChartRef = ref<HTMLDivElement | null>(null);
let barChartInstance: echarts.ECharts | null = null;

const barChartConfig = {
  backgroundColor: 'transparent',
  title: {
    text: '股票收益预测',
    left: 'center'
  },
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  xAxis: {
    type: 'category',
    data: [stockDetail.value.year1, stockDetail.value.year2, stockDetail.value.year3, stockDetail.value.year4],
    name: ' ',
    nameLocation: 'middle',
    nameGap: 25
  },
  yAxis: {
    type: 'value',
    name: '每股收益 (EPS)',
    nameLocation: 'middle',
    nameGap: 40
  },
  series: [
    {
      data: [stockDetail.value.eps1, stockDetail.value.eps2, stockDetail.value.eps3, stockDetail.value.eps4],
      type: 'bar',
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#ff7f0e' },
          { offset: 0.5, color: '#ff5722' },
          { offset: 1, color: '#e64a19' }
        ])
      },
      emphasis: {
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#ff5722' },
            { offset: 0.7, color: '#e64a19' },
            { offset: 1, color: '#d84315' }
          ])
        }
      },
      animationDelay(idx) {
        return idx * 200;
      }
    }
  ]
};

// 监听 stockDetailData 的变化，并更新图表
watch(stockDetailData, () => {
  updatePieChart();
  updateBarChart();
});

// 更新饼状图的方法
function updatePieChart() {
  const pieChartConfig2 = {
    backgroundColor: 'transparent',
    series: [
      {
        type: 'pie',
        radius: '40%',
        data: [
          { value: stockDetailData.value.ratingBuyNum, name: '买进指数', itemStyle: { color: '#d62728' } },
          { value: stockDetailData.value.ratingAddNum, name: '增持指数', itemStyle: { color: '#ff7f0e' } },
          { value: stockDetailData.value.ratingNeutralNum, name: '观望指数', itemStyle: { color: '#2ca02c' } },
          { value: stockDetailData.value.ratingReduceNum, name: '减持指数', itemStyle: { color: '#9467bd' } },
          { value: stockDetailData.value.ratingSaleNum, name: '卖出指数', itemStyle: { color: '#1f77b4' } }
        ].filter(item => item.value > 0),
        label: {
          fontSize: 10,
          formatter: params => `${params.name}: ${params.value}`
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  };
  chartInstance.setOption(pieChartConfig2, true);
}

// 更新条形图的方法
function updateBarChart() {
  const barChartConfig2 = {
    backgroundColor: 'transparent',
    title: {
      text: '股票收益预测',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    xAxis: {
      type: 'category',
      data: [
        stockDetailData.value.year1,
        stockDetailData.value.year2,
        stockDetailData.value.year3,
        stockDetailData.value.year4
      ],
      name: ' ',
      nameLocation: 'middle',
      nameGap: 25
    },
    yAxis: {
      type: 'value',
      name: '每股收益 (EPS)',
      nameLocation: 'middle',
      nameGap: 40
    },
    series: [
      {
        data: [
          stockDetailData.value.eps1,
          stockDetailData.value.eps2,
          stockDetailData.value.eps3,
          stockDetailData.value.eps4
        ],
        type: 'bar',
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#ff7f0e' },
            { offset: 0.5, color: '#ff5722' },
            { offset: 1, color: '#e64a19' }
          ])
        },
        emphasis: {
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: '#ff5722' },
              { offset: 0.7, color: '#e64a19' },
              { offset: 1, color: '#d84315' }
            ])
          }
        },
        animationDelay: idx => idx * 200
      }
    ]
  };
  barChartInstance.setOption(barChartConfig2, true);
}

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    chartInstance.setOption(pieChartConfig);
  }
  if (barChartRef.value) {
    barChartInstance = echarts.init(barChartRef.value);
    barChartInstance.setOption(barChartConfig);
  }
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
  if (barChartInstance) {
    barChartInstance.dispose();
  }
});

const lineChartRef = ref<HTMLDivElement | null>(null);
let lineChartInstance: echarts.ECharts | null = null;

// 定义图表配置
const getLineChartConfig = data => {
  return {
    backgroundColor: 'transparent',
    title: {
      text: '股票年报数据 ',
      left: 'center',
      top: '2%'
    },
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['营业总收入', '归母净利润', '扣非归母净利润'],
      top: '8%'
    },
    xAxis: {
      type: 'category',
      data: Object.keys(data.financialDataByYear),
      name: ' ',
      nameLocation: 'middle',
      nameGap: 25
    },
    yAxis: [
      {
        type: 'value',
        name: '营业总收入',
        nameLocation: 'middle',
        nameGap: 40,
        axisLabel: {
          formatter: '{value}'
        }
      },
      {
        type: 'value',
        name: '归母净利润/扣非归母净利润',
        nameLocation: 'middle',
        nameGap: 60,
        axisLabel: {
          formatter: '{value}'
        }
      }
    ],
    series: [
      {
        name: '营业总收入',
        type: 'line',
        yAxisIndex: 0,
        data: Object.values(data.financialDataByYear).map(yearData => yearData.totalOperatereveIncrease),
        itemStyle: {
          color: '#ff0000'
        }
      },
      {
        name: '归母净利润',
        type: 'line',
        yAxisIndex: 1,
        data: Object.values(data.financialDataByYear).map(yearData => yearData.parentNetprofitIncrease),
        itemStyle: {
          color: '#00ff00'
        }
      },
      {
        name: '扣非归母净利润',
        type: 'line',
        yAxisIndex: 1,
        data: Object.values(data.financialDataByYear).map(yearData => yearData.dnetprofitatpcTcalIncrease),
        itemStyle: {
          color: '#0000ff'
        }
      }
    ],
    animationEasing: 'linear',
    animationDuration: 2000
  };
};
const lineChartConfig = {
  backgroundColor: 'transparent',
  title: {
    text: '股票年报数据 ',
    left: 'center',
    top: '2%'
  },
  tooltip: {
    trigger: 'axis'
  },
  legend: {
    data: ['营业总收入', '归母净利润', '扣非归母净利润'],
    top: '8%'
  },
  xAxis: {
    type: 'category',
    data: Object.keys(stockInfo.value.financialDataByYear),
    name: ' ',
    nameLocation: 'middle',
    nameGap: 25
  },
  yAxis: [
    {
      type: 'value',
      name: '营业总收入',
      nameLocation: 'middle',
      nameGap: 40,
      axisLabel: {
        formatter: '{value}'
      }
    },
    {
      type: 'value',
      name: '归母净利润/扣非归母净利润',
      nameLocation: 'middle',
      nameGap: 60,
      axisLabel: {
        formatter: '{value}'
      }
    }
  ],
  series: [
    {
      name: '营业总收入',
      type: 'line',
      yAxisIndex: 0,
      data: Object.values(stockInfo.value.financialDataByYear).map(yearData => yearData.totalOperatereveIncrease),
      areaStyle: {},
      itemStyle: {
        color: '#ff0000'
      },
      animationDelay(idx) {
        return idx * 200;
      }
    },
    {
      name: '归母净利润',
      type: 'line',
      yAxisIndex: 1,
      data: Object.values(stockInfo.value.financialDataByYear).map(yearData => yearData.parentNetprofitIncrease),
      itemStyle: {
        color: '#00ff00'
      },
      animationDelay(idx) {
        return idx * 200;
      }
    },
    {
      name: '扣非归母净利润',
      type: 'line',
      yAxisIndex: 1,
      data: Object.values(stockInfo.value.financialDataByYear).map(yearData => yearData.dnetprofitatpcTcalIncrease),
      itemStyle: {
        color: '#0000ff'
      },
      animationDelay(idx) {
        return idx * 200;
      }
    }
  ],
  animationEasing: 'linear',
  animationDuration: 2000
};
watch(stockInfoData, newData => {
  if (lineChartInstance && newData && newData.financialDataByYear) {
    const chartConfig = getLineChartConfig(newData);
    lineChartInstance.setOption(chartConfig, true);
  }
});
onMounted(() => {
  if (lineChartRef.value) {
    lineChartInstance = echarts.init(lineChartRef.value);
    lineChartInstance.setOption(lineChartConfig);
  }
});

onUnmounted(() => {
  if (lineChartInstance) {
    lineChartInstance.dispose();
  }
});

const computedLatestPrice = computed(() => {
  const price = Number.parseFloat(stockDetailData.value.latestPrice);
  return isNaN(price) ? 0 : price; // 如果是NaN，则默认为0
});

const computedPriceChange = computed(() => {
  const change = Number.parseFloat(stockDetailData.value.priceChange);
  return isNaN(change) ? 0 : change;
});

const computedPriceChangeRate = computed(() => {
  const rate = Number.parseFloat(stockDetailData.value.priceChangeRate);
  return isNaN(rate) ? 0 : rate;
});
const onAdd = async code => {
  try {
    const response = await request({
      url: '/favor',
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      data: {
        stockCode: code
      }
    });
    console.log(response);
    if (response) {
      alert('添加成功');
    } else {
      alert('已在自选股中');
    }
  } catch (error) {
    // alert('已在自选股中');
  }
};
</script>

<template>
  <div>
    <ATooltip placement="right">
      <template #title>返回</template>
      <AButton shape="circle" @click="goBack"><icon-ic:outline-keyboard-arrow-left class="h-8 w-8 pb-2" /></AButton>
    </ATooltip>
    <ARow class="flex justify-between">
      <ACard :bordered="false" class="mt-2 w-35% card-wrapper">
        <div class="flex justify-between">
          <div>
            <div class="mb--1 text-5 font-bold">{{ stockDetailData.stockName }}</div>
            <div class="text-4">{{ stockDetailData.stockCode }}</div>
            <div class="flex-x-center text-4">{{ stockInfoData.summary }}</div>
          </div>
          <div>
            <div>
              <CountTo
                suffix=""
                :start-value="1"
                :end-value="computedLatestPrice"
                :decimals="2"
                class="text-6 font-sans"
                :class="computedPriceChange >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'"
              />
            </div>
            <div class="mt--2 flex justify-between">
              <CountTo
                suffix=""
                :start-value="1"
                :end-value="computedPriceChange"
                :decimals="2"
                class="text-3 font-sans"
                :class="computedPriceChange >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'"
              />
              <CountTo
                suffix="%"
                :start-value="1"
                :end-value="computedPriceChangeRate"
                :decimals="2"
                class="ml-1.5 text-3 font-sans"
                :class="computedPriceChange >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'"
              />
            </div>
          </div>
          <ATooltip placement="topRight">
            <template #title>加入自选</template>
            <AButton class="mt-2" type="primary" shape="circle" size="large" @click="() => onAdd(stockCode)">
              <icon-material-symbols-light:add-rounded class="mt--2.5 h-12 w-10" />
            </AButton>
          </ATooltip>
        </div>
        <div class="mb-2 mt-5 w-full flex-x-center text-5 font-bold">
          投资评级
          <icon-tdesign:compass class="ml-1 mt-2" />
        </div>
        <div ref="chartRef" class="chart-container mb--17 mt--14 flex-x-center"></div>
      </ACard>
      <ACard :bordered="false" class="mt-2 w-60% card-wrapper">
        <div ref="barChartRef" class="bar-chart-container mb--14 mt--5 flex-x-center"></div>
      </ACard>
    </ARow>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <div ref="lineChartRef" class="line-chart-container mb--14 mt--5 flex-x-center"></div>
    </ACard>
  </div>
</template>

<style scoped>
.chart-container {
  width: 100%; /* 缩小图表宽度 */
  height: 15rem; /* 缩小图表高度 */
}
.bar-chart-container {
  width: 100%;
  height: 18rem;
}
.line-chart-container {
  width: 100%;
  height: 20rem;
}
</style>
(: { data: any; })(: { data: any; }): { name: any; value: any; }: number: number: number: number
