<script setup lang="ts">
import { onMounted, onUnmounted, ref, watch } from 'vue';
import * as echarts from 'echarts';

interface CorrelationData {
  date: string;
  sentimentChange: number;
  priceChange: number;
  correlationSummary: string;
  sentimentCount: number;
}

interface Props {
  correlationData: CorrelationData[];
}

const props = defineProps<Props>();

const chartRef = ref<HTMLDivElement | null>(null);
let chartInstance: echarts.ECharts | null = null;

const updateChart = () => {
  if (!props.correlationData?.length) return;

  // 添加数据检查日志
  console.log('Raw Correlation Data:', props.correlationData);

  // 数据预处理和对齐
  const dates = props.correlationData.map(item => item.date);
  const sentimentChanges = props.correlationData.map(item => {
    // 检查字段名和值
    console.log('Processing item:', item);
    const value = item.sentimentChange;  // 使用正确的字段名
    console.log('Sentiment change value:', value);
    return typeof value === 'string' ? parseFloat(value) : (value || 0);
  });
  const priceChanges = props.correlationData.map(item => {
    const value = item.priceChange;
    return typeof value === 'string' ? parseFloat(value) : (value || 0);
  });
  const commentCounts = props.correlationData.map(item =>
    typeof item.sentimentCount === 'string' ? parseInt(item.sentimentCount) : (item.sentimentCount || 0)
  );

  // 检查处理后的数据
  console.log('Processed Data:', {
    dates: dates.slice(0, 5),
    sentimentChanges: sentimentChanges.slice(0, 5),
    priceChanges: priceChanges.slice(0, 5),
    commentCounts: commentCounts.slice(0, 5)
  });

  const option = {
    backgroundColor: 'transparent',
    title: {
      text: '情感变化-股价变动分析',
      left: 'center',
      top: 0,
      textStyle: {
        fontSize: 18,
        fontWeight: 'bold'
      },
      subtext: "分析结果：" + props.correlationData[0]?.correlationSummary || '',
      subtextStyle: {
        color: '#666',
        fontSize: 14,
        padding: [5, 0, 30, 0]
      }
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'line'
      },
      formatter: function (params: any[]) {
        const date = params[0].axisValue;
        let result = `${date}<br/>`;
        params.forEach(param => {
          if (param.seriesName === '评论数') {
            result += `${param.seriesName}: ${param.value}<br/>`;
          } else {
            result += `${param.seriesName}: ${param.value.toFixed(4)}${param.seriesName === '股价变动' ? '%' : ''}<br/>`;
          }
        });
        return result;
      }
    },
    legend: {
      data: ['情感变化', '股价变动', '评论数'],
      top: '80px'
    },
    grid: {
      left: '5%',
      right: '10%',
      bottom: '10%',
      top: '30%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      scale: true,
      boundaryGap: false,
      axisLine: { onZero: false },
      splitLine: { show: false },
      min: 'dataMin',
      max: 'dataMax',
      axisLabel: {
        formatter: (value: string) => {
          return value; // 显示完整日期
        }
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '情感变化',
        position: 'left',
        scale: true,
        splitLine: {
          show: true,
          lineStyle: {
            type: 'dashed',
            opacity: 0.3
          }
        },
        axisLabel: {
          formatter: (value: number) => value.toFixed(3)
        }
      },
      {
        type: 'value',
        name: '股价变动(%)',
        position: 'right',
        splitLine: {
          show: false
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: '#91cc75'
          }
        }
      },
      {
        type: 'value',
        name: '评论数',
        position: 'right',
        offset: 80,
        splitLine: {
          show: false
        },
        axisLine: {
          show: true,
          lineStyle: {
            color: '#fac858'
          }
        }
      }
    ],
    series: [
      {
        name: '情感变化',
        type: 'line',
        data: sentimentChanges,
        yAxisIndex: 0,
        symbol: 'circle',
        symbolSize: 4,
        sampling: 'lttb',
        itemStyle: {
          color: '#5470c6'
        },
        lineStyle: {
          width: 1.5
        },
        markLine: {
          silent: true,
          data: [{
            yAxis: 0,
            lineStyle: {
              color: '#5470c6',
              type: 'dashed',
              opacity: 0.5
            }
          }]
        }
      },
      {
        name: '股价变动',
        type: 'line',
        data: priceChanges,
        yAxisIndex: 1,
        symbol: 'circle',
        symbolSize: 4,
        sampling: 'lttb',
        itemStyle: {
          color: '#91cc75'
        },
        lineStyle: {
          width: 1.5
        },
        markLine: {
          silent: true,
          data: [{
            yAxis: 0,
            lineStyle: {
              color: '#91cc75',
              type: 'dashed',
              opacity: 0.5
            }
          }]
        }
      },
      {
        name: '评论数',
        type: 'bar',
        data: commentCounts,
        yAxisIndex: 2,
        itemStyle: {
          color: '#fac858'
        },
        barWidth: '60%',
        opacity: 0.7
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        start: 0,
        end: 100
      },
      {
        show: true,
        type: 'slider',
        bottom: '3%',
        start: 0,
        end: 100
      }
    ]
  };

  // 添加图表选项检查日志
  console.log('Chart Option:', option);

  chartInstance?.setOption(option, true);
};

// 添加 props 数据监听日志
watch(() => props.correlationData, (newVal) => {
  console.log('Correlation Data Changed:', newVal?.slice(0, 5));
  if (newVal?.length && chartInstance) {
    updateChart();
  }
}, { deep: true });

onMounted(() => {
  if (chartRef.value) {
    chartInstance = echarts.init(chartRef.value);
    window.addEventListener('resize', handleResize);
    if (props.correlationData?.length) {
      updateChart();
    }
  }
});

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose();
  }
  window.removeEventListener('resize', handleResize);
});

const handleResize = () => {
  chartInstance?.resize();
};
</script>

<template>
  <div class="correlation-chart">
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<style scoped>
.correlation-chart {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chart-container {
  width: 100%;
  height: 400px;
}
</style>
