<script setup lang="ts">
import { useRoute, useRouter } from 'vue-router';
import { computed, onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';
import { request } from '@/service/request';
import 'echarts-wordcloud';
// import { fetchStockDataAndPrediction, fetchStockFinancialData } from '@/service/api/stock-detail';

// 定义接口类型
interface StockDetailData {
  stockCode: string;
  stockName: string;
  latestPrice: string;
  priceChangeRate: string;
  priceChange: string;
  riseSpeed: string;
  ratingOrgNum: number;
  ratingBuyNum: number;
  ratingAddNum: number;
  ratingNeutralNum: number;
  ratingReduceNum: number;
  ratingSaleNum: number;
  year1: number;
  eps1: number;
  year2: number;
  eps2: number;
  year3: number;
  eps3: number;
  year4: number;
  eps4: number;
}

interface StockInfoData {
  stockCode: string;
  summary: string;
  financialDataByYear: Record<string, any>;
}

const stockDetailData = ref<StockDetailData>({} as StockDetailData);
const stockInfoData = ref<StockInfoData>({} as StockInfoData);
const klineData = ref([]);

const route = useRoute();
const router = useRouter();
const stockCode = route.query.stockCode;
console.log(stockCode);

// const routeQuery = computed(() => JSON.stringify(route.query));

async function fetchStockFinancialData(stockCode: string) {
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
    if (result?.data) {
      stockInfoData.value = result.data;
    }
  } catch (error) {
    console.error('Error fetching financial data:', error);
  }
}

async function fetchstockDetailData(stockCode: string) {
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
    if (result?.data) {
      stockDetailData.value = result.data;
    }
  } catch (error) {
    console.error('Error fetching stock detail:', error);
  }
}

async function fetchKlineData(stockCode) {
  try {
    const result = await request({
      url: '/stock/kline',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        stockCode
      },
      method: 'GET'
    });
    if (result) {
      klineData.value = result.data;
      updateKlineChart();
    }
  } catch (error) {
    console.error('Error fetching kline data:', error);
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
        { value: stockDetail.value.ratingBuyNum, name: '买入', itemStyle: { color: '#d62728' } }, // 红色
        { value: stockDetail.value.ratingAddNum, name: '增持', itemStyle: { color: '#ff7f0e' } }, // 橙色
        { value: stockDetail.value.ratingNeutralNum || 0, name: '观望', itemStyle: { color: '#2ca02c' } }, // 绿色
        { value: stockDetail.value.ratingReduceNum || 0, name: '减持', itemStyle: { color: '#9467bd' } }, // 紫色
        { value: stockDetail.value.ratingSaleNum || 0, name: '卖出', itemStyle: { color: '#1f77b4' } } // 蓝色
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
  if (klineChartRef.value) {
    klineChartInstance = echarts.init(klineChartRef.value);
    fetchKlineData(stockCode);
  }
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
  if (klineChartInstance) {
    klineChartInstance.dispose();
  }
});

window.addEventListener('resize', () => {
  klineChartInstance?.resize();
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
          { value: stockDetailData.value.ratingBuyNum, name: '买入', itemStyle: { color: '#d62728' } },
          { value: stockDetailData.value.ratingAddNum, name: '增持', itemStyle: { color: '#ff7f0e' } },
          { value: stockDetailData.value.ratingNeutralNum, name: '观望', itemStyle: { color: '#2ca02c' } },
          { value: stockDetailData.value.ratingReduceNum, name: '减持', itemStyle: { color: '#9467bd' } },
          { value: stockDetailData.value.ratingSaleNum, name: '卖出', itemStyle: { color: '#1f77b4' } }
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

// 添加K线图的ref和实例
const klineChartRef = ref<HTMLDivElement | null>(null);
let klineChartInstance: echarts.ECharts | null = null;

// 修改K线图配置和更新函数
function updateKlineChart() {
  // 如果没有K线数据，直接返回
  if (!klineData.value?.length) {
    return;
  }

  // 基础配置
  const klineOption = {
    backgroundColor: 'transparent',
    title: {
      // 根据是否有情感数据来设置标题
      text: sentimentData.value?.length ? 'K线图与评论情感趋势' : 'K线图',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function (params) {
        const date = params[0].axisValue;
        let res = `${date}<br/>`;
        params.forEach(param => {
          if (param.seriesName === 'K线') {
            res += `${param.seriesName}: 开盘${param.data[1]}, 收盘${param.data[2]}, 最低${param.data[3]}, 最高${param.data[4]}<br/>`;
          } else {
            res += `${param.seriesName}: ${param.data}<br/>`;
          }
        });
        return res;
      }
    },
    legend: {
      // 根据是否有情感数据来设置图例
      data: sentimentData.value?.length ? ['K线', '情感值', '评论数'] : ['K线'],
      top: '30px'
    },
    grid: {
      left: '10%',
      right: sentimentData.value?.length ? '10%' : '5%', // 如果没有情感数据，可以减少右边距
      bottom: '15%'
    },
    xAxis: {
      type: 'category',
      data: klineData.value.map(item => item.dateTime),
      scale: true,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax'
    },
    yAxis: [
      {
        scale: true,
        splitArea: {
          show: true
        }
      },
      // 只在有情感数据时添加额外的y轴
      ...(sentimentData.value?.length ? [
        {
          scale: true,
          name: '情感值',
          min: 0,
          max: 1,
          position: 'right',
          offset: 80,
          axisLine: {
            show: true,
            lineStyle: {
              color: '#ff7f0e'
            }
          },
          axisLabel: {
            formatter: '{value}'
          }
        },
        {
          scale: true,
          name: '评论数',
          position: 'right',
          offset: 160,
          axisLine: {
            show: true,
            lineStyle: {
              color: '#2ca02c'
            }
          },
          axisLabel: {
            formatter: '{value}'
          }
        }
      ] : [])
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 50,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        bottom: '3%',
        start: 50,
        end: 100
      }
    ],
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: klineData.value.map(item => [
          item.openPrice,
          item.closePrice,
          item.lowPrice,
          item.highPrice
        ]),
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        }
      }
    ]
  };

  // 只在有情感数据时添加情感相关的系列
  if (sentimentData.value?.length) {
    const dateMap = new Map();
    sentimentData.value.forEach(item => {
      dateMap.set(item.date, item);
    });

    const alignedSentimentData = klineData.value.map(kline => {
      const sentiment = dateMap.get(kline.dateTime);
      return sentiment ? sentiment.sentimentAvg : null;
    });

    const alignedCommentData = klineData.value.map(kline => {
      const sentiment = dateMap.get(kline.dateTime);
      return sentiment ? sentiment.commentCount : null;
    });

    klineOption.series.push(
      {
        name: '情感值',
        type: 'line',
        yAxisIndex: 1,
        data: alignedSentimentData,
        smooth: true,
        lineStyle: {
          width: 2
        },
        itemStyle: {
          color: '#ff7f0e'
        }
      },
      {
        name: '评论数',
        type: 'bar',
        yAxisIndex: 2,
        data: alignedCommentData,
        itemStyle: {
          color: '#2ca02c'
        }
      }
    );
  }

  klineChartInstance?.setOption(klineOption);
}

// 修改数据加载逻辑
onMounted(async () => {
  // ... 其他初始化代码 ...

  if (klineChartRef.value) {
    klineChartInstance = echarts.init(klineChartRef.value);
    // 先加载K线数据
    await fetchKlineData(stockCode);
    // 再加载情感数据
    await fetchSentimentData(stockCode);
  }

  if (wordCloudRef.value) {
    wordCloudInstance = echarts.init(wordCloudRef.value);
    fetchWordFrequencyData(stockCode);
  }
});

// 修改fetchSentimentData函数
async function fetchSentimentData(stockCode) {
  try {
    const result = await request({
      url: '/stock/sentiment',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        stockCode
      },
      method: 'GET'
    });
    if (result) {
      sentimentData.value = result.data;
      // 确保K线数据已加载后再更新图表
      if (klineData.value?.length) {
        updateKlineChart();
      }
    }
  } catch (error) {
    console.error('Error fetching sentiment data:', error);
  }
}

// 添加新的响应式数据
const sentimentData = ref([]);
const wordFreqData = ref([]);

// 添加新的请求函数
async function fetchWordFrequencyData(stockCode) {
  try {
    const result = await request({
      url: '/stock/word-frequency',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        stockCode
      },
      method: 'GET'
    });
    if (result) {
      wordFreqData.value = result.data;
      updateWordCloudChart();
    }
  } catch (error) {
    console.error('Error fetching word frequency data:', error);
  }
}

// 添加图表ref和实例
const sentimentChartRef = ref<HTMLDivElement | null>(null);
const wordCloudChartRef = ref<HTMLDivElement | null>(null);
let sentimentChartInstance: echarts.ECharts | null = null;
let wordCloudChartInstance: echarts.ECharts | null = null;
// 添加新的响应式数据
const correlationData = ref([]);
const correlationChartRef = ref<HTMLDivElement | null>(null);
let correlationChartInstance: echarts.ECharts | null = null;

// 更新词云图表
function updateWordCloudChart() {
  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '评论关键词',
      left: 'center'
    },
    tooltip: {
      show: true
    },
    series: [{
      type: 'wordCloud',
      shape: 'circle',
      left: 'center',
      top: 'center',
      width: '70%',
      height: '80%',
      right: null,
      bottom: null,
      sizeRange: [12, 60],
      rotationRange: [-90, 90],
      rotationStep: 45,
      gridSize: 8,
      drawOutOfBound: false,
      textStyle: {
        fontFamily: 'sans-serif',
        fontWeight: 'bold',
        color: function () {
          return 'rgb(' + [
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160),
            Math.round(Math.random() * 160)
          ].join(',') + ')';
        }
      },
      emphasis: {
        focus: 'self',
        textStyle: {
          shadowBlur: 10,
          shadowColor: '#333'
        }
      },
      data: wordFreqData.value.map(item => ({
        name: item.word,
        value: item.frequency,
        textStyle: {
          color: `rgb(${Math.round(Math.random() * 160)},${Math.round(Math.random() * 160)},${Math.round(Math.random() * 160)})`
        }
      }))
    }]
  };

  wordCloudChartInstance?.setOption(option);
}

// 修改onMounted钩子
onMounted(() => {
  // ... 原有的初始化代码 ...

  if (sentimentChartRef.value) {
    sentimentChartInstance = echarts.init(sentimentChartRef.value);
    fetchSentimentData(stockCode);
  }

  if (wordCloudChartRef.value) {
    wordCloudChartInstance = echarts.init(wordCloudChartRef.value);
    fetchWordFrequencyData(stockCode);
  }

  if (correlationChartRef.value) {
    correlationChartInstance = echarts.init(correlationChartRef.value);
    fetchSentimentCorrelation(stockCode);
  }
});

// 修改onUnmounted钩子
onUnmounted(() => {
  // ... 原有的销毁代码 ...
  sentimentChartInstance?.dispose();
  wordCloudChartInstance?.dispose();
  correlationChartInstance?.dispose();
});


// 添加新的请求函数
async function fetchSentimentCorrelation(stockCode) {
  try {
    const result = await request({
      url: '/stock/sentiment-correlation',
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      params: {
        stockCode
      },
      method: 'GET'
    });
    if (result) {
      correlationData.value = result.data;
      updateCorrelationChart();
    }
  } catch (error) {
    console.error('Error fetching correlation data:', error);
  }
}

// 添加图表更新函数
function updateCorrelationChart() {
  if (!correlationData.value?.length) return;

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '情感-股价相关性分析',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      }
    },
    legend: {
      data: ['情感值', '次日股价变动'],
      top: '30px'
    },
    xAxis: {
      type: 'category',
      data: correlationData.value.map(item => item.date)
    },
    yAxis: [
      {
        type: 'value',
        name: '情感值',
        position: 'left'
      },
      {
        type: 'value',
        name: '股价变动(%)',
        position: 'right'
      }
    ],
    series: [
      {
        name: '情感值',
        type: 'line',
        data: correlationData.value.map(item => item.sentimentAvg),
        yAxisIndex: 0
      },
      {
        name: '次日股价变动',
        type: 'line',
        data: correlationData.value.map(item => item.nextDayPriceChange),
        yAxisIndex: 1
      }
    ]
  };

  correlationChartInstance?.setOption(option);
}

window.addEventListener('resize', () => {
  correlationChartInstance?.resize();
});
</script>

// 在template中添加图表容器
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
            <div class="mb--1 text-5 font-bold">{{ stockDetailData?.stockName || '-' }}</div>
            <div class="text-4">{{ stockDetailData?.stockCode || '-' }}</div>
            <div class="flex-x-center text-4">{{ stockInfoData?.summary || '-' }}</div>
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
          近期证券机构研报评级分布
          <icon-tdesign:compass class="ml-1 mt-2" />
        </div>
        <div ref="chartRef" class="chart-container mb--17 mt--14 flex-x-center"></div>
      </ACard>
      <ACard :bordered="false" class="mt-2 w-60% card-wrapper">
        <div ref="barChartRef" class="bar-chart-container mb--14 mt--5 flex-x-center"></div>
      </ACard>
    </ARow>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <div ref="klineChartRef" class="kline-chart-container"></div>
    </ACard>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <div ref="correlationChartRef" class="correlation-chart-container"></div>
    </ACard>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <div ref="lineChartRef" class="line-chart-container mb--14 mt--5 flex-x-center"></div>
    </ACard>
    <ACard :bordered="false" class="mt-4 w-full card-wrapper">
      <div ref="wordCloudChartRef" class="wordcloud-chart-container"></div>
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
.kline-chart-container {
  width: 100%;
  height: 400px;
}
.sentiment-chart-container,
.wordcloud-chart-container {
  width: 100%;
  height: 400px;
}
.correlation-chart-container {
  width: 100%;
  height: 400px;
}
</style>
