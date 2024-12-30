<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  stockDetailData: {
    stockName: string;
    stockCode: string;
    latestPrice: string;
    priceChange: string;
    priceChangeRate: string;
  };
  stockInfoData: {
    summary: string;
  };
  stockCode: string;
}

const props = defineProps<Props>();

const computedLatestPrice = computed(() => {
  const price = Number.parseFloat(props.stockDetailData.latestPrice);
  return Number.isNaN(price) ? 0 : price;
});

const computedPriceChange = computed(() => {
  const change = Number.parseFloat(props.stockDetailData.priceChange);
  return Number.isNaN(change) ? 0 : change;
});

const computedPriceChangeRate = computed(() => {
  const rate = Number.parseFloat(props.stockDetailData.priceChangeRate);
  return Number.isNaN(rate) ? 0 : rate;
});

const emit = defineEmits(['add']);
const onAdd = (code: string) => {
  emit('add', code);
};
</script>

<template>
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
</template>
