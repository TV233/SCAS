<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import { useTransition } from '@vueuse/core';

const duration = 6500;
interface Props {
  decrease?: number;
  increase?: number;
}
const props = withDefaults(defineProps<Props>(), {
  decrease: 1234,
  increase: 1234
});
const upNumber = ref(0);
const downNumber = ref(0);
const total = computed(() => props.increase + props.decrease);

const cubicBezierNumber = useTransition(
  computed(() => (props.increase / total.value) * 100),
  {
    duration,
    transition: [0.75, 0, 0.25, 1]
  }
);

const cubicBezierNumber2 = useTransition(
  computed(() => (props.decrease / total.value) * 100),
  {
    duration,
    transition: [0.75, 0, 0.25, 1]
  }
);

onMounted(() => toggle());
function toggle() {
  upNumber.value = props.increase;
  downNumber.value = props.decrease;
}
</script>

<template>
  <div>
    <div class="mb--2 mt-2 flex justify-between text-5">
      <span class="text-[#fe2435]">
        涨
        <CountTo :start-value="1" :end-value="props.increase" class="ml--1.5" />
      </span>
      <span class="text-[#08aa4b]">
        跌
        <CountTo :start-value="1" :end-value="props.decrease" class="ml--1.5" />
      </span>
    </div>
    <div class="track number">
      <div class="relative flex justify-between">
        <div class="sled" :style="{ width: `${cubicBezierNumber}%` }" />
        <div class="down" :style="{ width: `${cubicBezierNumber2}%` }" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.track {
  background: rgba(125, 125, 125, 0.3);
  border-radius: 0.5rem;
  width: 100%;
}

.sled {
  background: red;
  height: 1.25rem;
  border-top-left-radius: 0.5rem;
  border-bottom-left-radius: 0.5rem;
  width: 1rem;
  clip-path: polygon(0 0, calc(100% - 10px) 0, 100% 100%, 0 100%);
}

.down {
  background: green;
  border-top-right-radius: 0.5rem;
  border-bottom-right-radius: 0.5rem;
  height: 1.25rem;
  clip-path: polygon(0 0, 100% 0, 100% 100%, 10px 100%);
  width: 1rem;
}

.number.track {
  height: 1.25rem;
  margin: 0.5rem 0;
}
</style>
