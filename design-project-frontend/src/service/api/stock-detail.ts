import { request } from '../request';

/**
 * 获取股票年报数据
 *
 * @param stockCode 股票代码
 */
export function fetchStockFinancialData(stockCode: string) {
  return request<Api.StockDetail.FinancialData>({
    url: '/stock/financial_data',
    method: 'get',
    params: {
      stockCode
    }
  });
}

/**
 * 获取股票实时涨跌数据和预测数据
 *
 * @param stockCode 股票代码
 */
export function fetchStockDataAndPrediction(stockCode: string) {
  return request<Api.StockDetail.DataAndPrediction>({
    url: '/stock',
    method: 'get',
    params: {
      stockCode
    }
  });
}
