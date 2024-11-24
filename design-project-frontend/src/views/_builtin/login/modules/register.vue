<script setup lang="ts">
import { computed, reactive } from 'vue';
import { $t } from '@/locales';
import { useRouterPush } from '@/hooks/common/router';
import { request } from '@/service/request';
import { useAntdForm, useFormRules } from '@/hooks/common/form';
// import { useAuthStore } from '@/store/modules/auth';
// import { useCaptcha } from '@/hooks/business/captcha';

defineOptions({
  name: 'Register'
});

// const authStore = useAuthStore();
const { toggleLoginModule } = useRouterPush();
const { formRef, validate } = useAntdForm();
// const { label, isCounting, loading, getCaptcha } = useCaptcha();

interface FormModel {
  userName: string;
  // code: string;
  password: string;
  confirmPassword: string;
}

const model: FormModel = reactive({
  userName: '',
  // code: '',
  password: '',
  confirmPassword: ''
});

const rules = computed<Record<keyof FormModel, App.Global.FormRule[]>>(() => {
  const { formRules, createConfirmPwdRule } = useFormRules();

  return {
    userName: formRules.userName,
    // code: formRules.code,
    password: formRules.pwd,
    confirmPassword: createConfirmPwdRule(model.password)
  };
});

async function handleSubmit() {
  try {
    await validate();

    // Prepare the data in application/x-www-form-urlencoded format
    const formData = new URLSearchParams();
    formData.append('username', model.userName);
    formData.append('password', model.password);

    // Send the request
    const response = await request({
      method: 'post',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      url: '/auth/register',
      data: formData
    });
    alert('注册成功');
    // Handle the response
    console.log('aa', response); // 没有收到回应

    console.log('a', response.data.code);
    if (response) {
      // alert('注册成功');
      // window.$message?.success(response.data.message || $t('page.login.common.registerSuccess'));
    } else {
      // window.$message?.error(response.data.message || $t('page.login.common.registerFail'));
    }
  } catch (error) {
    // window.$message?.error($t('page.login.common.networkError'));
  }
}
// async function handleSubmit() {
//   await validate();
//   // request to register
//   // await authStore.login(model.userName, model.password);
//   window.$message?.success($t('page.login.common.validateSuccess'));
// }
</script>

<template>
  <AForm ref="formRef" :model="model" :rules="rules">
    <AFormItem name="userNmae">
      <AInput v-model:value="model.userName" size="large" :placeholder="$t('page.login.common.userNamePlaceholder')" />
    </AFormItem>
    <!-- 无验证码,担心ddos攻击 -->
    <!--
 <AFormItem name="code">
      <div class="w-full flex-y-center gap-16px">
        <AInput v-model:value="model.code" size="large" :placeholder="$t('page.login.common.codePlaceholder')" />
        <AButton size="large" :disabled="isCounting" :loading="loading" @click="getCaptcha(model.phone)">
          {{ label }}
        </AButton>
      </div>
    </AFormItem>
-->
    <AFormItem name="password">
      <AInputPassword
        v-model:value="model.password"
        size="large"
        :placeholder="$t('page.login.common.passwordPlaceholder')"
      />
    </AFormItem>
    <AFormItem name="confirmPassword">
      <AInputPassword
        v-model:value="model.confirmPassword"
        size="large"
        :placeholder="$t('page.login.common.confirmPasswordPlaceholder')"
      />
    </AFormItem>
    <ASpace direction="vertical" size="large" class="w-full">
      <AButton type="primary" block size="large" shape="round" @click="handleSubmit">
        {{ $t('common.confirm') }}
      </AButton>
      <AButton block size="large" shape="round" @click="toggleLoginModule('pwd-login')">
        {{ $t('page.login.common.back') }}
      </AButton>
    </ASpace>
  </AForm>
</template>

<style scoped></style>
