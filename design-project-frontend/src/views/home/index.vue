<script setup lang="ts">
import HeaderBanner from './modules/header-banner.vue';
import CardData from './modules/card-data.vue';
import HotTopic from './modules/hot-topic.vue';
import MarketBlock from './modules/market-block.vue';
import BestRank from './modules/best-rank.vue';
</script>

<template>
  <ASpace direction="vertical" :size="16">
    <HeaderBanner />
    <CardData />
    <ARow :gutter="[16, 16]">
      <ACol :span="24" :lg="14">
        <HotTopic />
        <MarketBlock />
      </ACol>
      <ACol :span="24" :lg="10">
        <BestRank />
      </ACol>
    </ARow>
  </ASpace>
</template>

<style scoped></style>
