<!-- eslint-disable no-invalid-this -->
<script setup lang="ts">
import type { PropType } from 'vue';
import { computed, defineProps, onMounted, ref } from 'vue';
import { createReusableTemplate } from '@vueuse/core';
import { request } from '@/service/request';
import ProgressBar from './progress-bar.vue';

defineOptions({
  name: 'CardData'
});
const stockIndices = ref([]);
async function fetchStockIndices() {
  try {
    // Using the custom request function to fetch the emotion index
    const result = await request({
      url: '/api/stock_indices',
      method: 'GET'
    });
    // Assuming 'result' directly contains the 'emotionIndex' after response transformation
    if (result) {
      // console.log(result);
      stockIndices.value = result.data;
    } else {
      console.error('No data returned for emotion index');
    }
  } catch (error) {
    console.error('Error fetching emotion index:', error);
    // showErrorMsg(error.message); // Utilize the shared error handling function if necessary
  }
}
const upDowns = ref([]);
async function fetchUpDown() {
  try {
    // Using the custom request function to fetch the emotion index
    const result = await request({
      url: '/api/upDown',
      method: 'GET'
    });
    // Assuming 'result' directly contains the 'emotionIndex' after response transformation
    if (result) {
      console.log('bbb', result);
      upDowns.value = result.data;
    } else {
      // console.error('No data returned for emotion index');
    }
  } catch (error) {
    // console.error('Error fetching emotion index:', error);
    // showErrorMsg(error.message); // Utilize the shared error handling function if necessary
  }
}

const cardData = computed(() => {
  return stockIndices.value.map(index => ({
    key: index.id,
    symbol: index.symbol,
    title: index.name,
    value: index.indexValue,
    rate: index.changePercent,
    change: index.changeAmount,
    color: item => ({
      start: item.change >= 0 ? '#ffd0d3' : '#cde3d2',
      end: item.change >= 0 ? '#ffe9eb' : '#e6f6ec'
    })
  }));
});
// const cardData = computed<any>(() => [
//   {
//     key: 9,
//     symbol: '000001',
//     title: '上证指数',
//     value: 2994.73,
//     rate: 0.92,
//     change: 27.33,
//     color: (item: any) => ({
//       start: item.change >= 0 ? '#ffd0d3' : '#cde3d2',
//       end: item.change >= 0 ? '#ffe9eb' : '#e6f6ec'
//     })
//   },
//   {
//     key: 10,
//     symbol: '399001',
//     title: '深证成指',
//     value: 8899.17,
//     rate: 0.57,
//     change: 50.47,
//     color: (item: any) => ({
//       start: item.change >= 0 ? '#ffd0d3' : '#cde3d2',
//       end: item.change >= 0 ? '#ffe9eb' : '#e6f6ec'
//     })
//   },
//   {
//     key: 11,
//     symbol: '399006',
//     title: '创业板指',
//     value: 1682.69,
//     rate: -0.04,
//     change: -0.74,
//     color: (item: any) => ({
//       start: item.change >= 0 ? '#ffd0d3' : '#cde3d2',
//       end: item.change >= 0 ? '#ffe9eb' : '#e6f6ec'
//     })
//   },
//   {
//     key: 12,
//     symbol: '000300',
//     title: '沪深300',
//     value: 3478.18,
//     rate: 0.48,
//     change: 16.52,
//     color: (item: any) => ({
//       start: item.change >= 0 ? '#ffd0d3' : '#cde3d2',
//       end: item.change >= 0 ? '#ffe9eb' : '#e6f6ec'
//     })
//   }
// ]);
onMounted(() => {
  fetchStockIndices(); // 在组件挂载时获取股票指数数据
  fetchUpDown();
});

interface GradientBgProps {
  gradientColor: string;
}

const [DefineGradientBg, GradientBg] = createReusableTemplate<GradientBgProps>();

function getGradientColor(color: { start: string; end: string }) {
  return `linear-gradient(to bottom, ${color.start}, ${color.end})`;
}

</script>

<template>
  <ACard :bordered="false" size="small" class="card-wrapper">
    <!-- define component start: GradientBg -->
    <DefineGradientBg v-slot="{ $slots, gradientColor }">
      <div class="rd-8px px-16px pb-4px pt-8px text-white" :style="{ backgroundImage: gradientColor }">
        <component :is="$slots.default" />
      </div>
    </DefineGradientBg>
    <!-- define component end: GradientBg -->

    <ARow class="mb-1 text-4 font-bold font-sans">
      <icon-fxemoji:stockchart class="mr-1 mt-1" />
      股票指数概览
    </ARow>
    <Simplebar>
      <ARow :gutter="[16, 16]" class="flex-nowrap pb-4">
        <ACol v-for="item in cardData" :key="item.key" :span="24" :sm="6" :lg="3">
          <GradientBg :gradient-color="getGradientColor(item.color(item))" class="flex-1">
            <h3 class="w-full flex justify-center text-16px text-dark font-600">{{ item.title }}</h3>
            <div class="mt--2 flex justify-center">
              <CountTo
                :prefix="item.unit"
                :start-value="1"
                :end-value="item.value"
                :decimals="2"
                class="text-6"
                :class="item.change >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'"
              />
            </div>
            <div class="mt--2 flex justify-between">
              <CountTo
                :prefix="item.change >= 0 ? '+' : ''"
                :start-value="1"
                :end-value="item.change"
                :decimals="2"
                class="text-3 dark:text-white"
                :class="item.change >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'"
              />
              <CountTo
                suffix="%"
                :start-value="1"
                :end-value="item.rate"
                :decimals="2"
                class="text-3 dark:text-white"
                :class="item.change >= 0 ? 'text-[#fe2435]' : 'text-[#08aa4b]'"
              />
            </div>
          </GradientBg>
        </ACol>
      </ARow>
    </Simplebar>

    <ProgressBar :decrease="upDowns.negativeChange" :increase="upDowns.positiveChange" />
    <!-- <div class="mb--5 mt-2 h-12 text-4 font-bold font-sans">
      今日实时成交额
      <CountTo suffix="亿" :start-value="1" :end-value="5804" class="text-4 dark:text-white" />
    </div> -->
  </ACard>
</template>

<style scoped>
/* 美化滚动条 */
::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 5px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>
