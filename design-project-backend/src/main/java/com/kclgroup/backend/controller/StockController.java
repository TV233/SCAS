package com.kclgroup.backend.controller;

import com.kclgroup.backend.pojo.entity.*;
import com.kclgroup.backend.pojo.vo.*;
import com.kclgroup.backend.service.*;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/stock")
@Validated
public class StockController {
    @Autowired
    StockInfoService stockInfoService;
    @Autowired
    StockPricesService stockPricesService;
    @Autowired
    PredictService predictService;
    @Autowired
    FinancialDataService financialDataService;
    @Autowired
    StockKlineService stockKlineService;
    @Autowired
    SentimentTrendService sentimentTrendService;
    @Autowired
    WordFrequencyService wordFrequencyService;
    @Autowired
    private SentimentPriceCorrelationService sentimentPriceCorrelationService;
    @Autowired
    private PredictionService predictionService;

    //根据股票代码获取股票信息
    @GetMapping()
    public Result<StockInfoVo> getStockInfo(@RequestParam String stockCode) {
        StockInfo stockInfo = stockInfoService.getByStockCode(stockCode);
        if(stockInfo == null)return Result.error("股票代码不存在");

        StockInfoVo stockInfoVo = new StockInfoVo();
        stockInfoVo.setStockCode(stockCode);
        stockInfoVo.setStockName(stockInfoService.getByStockCode(stockCode).getStockName());
        stockInfoVo.setLatestPrice(stockPricesService.getLatestPrice(stockCode));
        stockInfoVo.setPriceChangeRate(stockPricesService.getPriceChangeRate(stockCode));
        stockInfoVo.setPriceChange(stockPricesService.getPriceChange(stockCode));
        stockInfoVo.setRiseSpeed(stockPricesService.getRiseSpeed(stockCode));
        stockInfoVo.setRatingOrgNum(predictService.getRatingOrgNum(stockCode));
        stockInfoVo.setRatingBuyNum(predictService.getRatingBuyNum(stockCode));
        stockInfoVo.setRatingAddNum(predictService.getRatingAddNum(stockCode));
        stockInfoVo.setRatingNeutralNum(predictService.getRatingNeutralNum(stockCode));
        stockInfoVo.setRatingReduceNum(predictService.getRatingReduceNum(stockCode));
        stockInfoVo.setRatingSaleNum(predictService.getRatingSaleNum(stockCode));
        stockInfoVo.setYear1(predictService.getYear1(stockCode));
        stockInfoVo.setEps1(predictService.getEps1(stockCode));
        stockInfoVo.setYear2(predictService.getYear2(stockCode));
        stockInfoVo.setEps2(predictService.getEps2(stockCode));
        stockInfoVo.setYear3(predictService.getYear3(stockCode));
        stockInfoVo.setEps3(predictService.getEps3(stockCode));
        stockInfoVo.setYear4(predictService.getYear4(stockCode));
        stockInfoVo.setEps4(predictService.getEps4(stockCode));
        return Result.success(stockInfoVo);
    }
    @GetMapping("/financial_data")
    public Result<FinancialDataVo> getFinancialData(@RequestParam String stockCode) {
        return Result.success(financialDataService.getFinancialDataByStockCode(stockCode));
    }

    //输入股票名，模糊搜索，返回可能的股票名和相应股票代码列表
    @GetMapping("/find")
    public Result<List<StockInfo>> findStock(@RequestParam String stockName) {
        List<StockInfo> stockInfo = stockInfoService.getStockInfoByStockName(stockName);
        return Result.success(stockInfo);
    }

    @GetMapping("/kline")
    public Result<List<KlineVo>> getKlineData(@RequestParam String stockCode) {
        List<KlineVo> stockKlines = stockKlineService.getStockKline(stockCode);
        return Result.success(stockKlines);
    }

    // 获取情感趋势数据
    @GetMapping("/sentiment")
    public Result<List<SentimentTrendVo>> getSentimentTrend(@RequestParam String stockCode) {
        try {
            List<SentimentTrendVo> trendData = sentimentTrendService.getSentimentTrend(stockCode);
            return Result.success(trendData);
        } catch (Exception e) {
            return Result.error("获取情感趋势数据失败：" + e.getMessage());
        }
    }

    // 获取词频数据
    @GetMapping("/word-frequency")
    public Result<List<WordFrequencyVo>> getWordFrequency(@RequestParam String stockCode) {
        try {
            List<WordFrequencyVo> wordFreqData = wordFrequencyService.getWordFrequency(stockCode);
            return Result.success(wordFreqData);
        } catch (Exception e) {
            return Result.error("获取词频数据失败：" + e.getMessage());
        }
    }

    @GetMapping("/sentiment-correlation")
    public Result<List<SentimentPriceCorrelationVo>> getSentimentCorrelation(@RequestParam String stockCode) {
        List<SentimentPriceCorrelation> data = sentimentPriceCorrelationService.getByStockCode(stockCode);
        return Result.success(data.stream()
            .map(item -> {
                SentimentPriceCorrelationVo vo = new SentimentPriceCorrelationVo();
                vo.setStockCode(item.getStockCode());
                vo.setDate(item.getDate());
                vo.setSentimentChange(item.getSentimentChange());
                vo.setPriceChange(item.getPriceChange());
                vo.setCorrelation(item.getCorrelation());
                vo.setSentimentCount(item.getSentimentCount());
                vo.setCorrelationSummary(item.getCorrelationSummary());
                return vo;
            })
            .collect(Collectors.toList()));
    }

    @GetMapping("/predictions/{stockCode}")
    public Result<List<PredictionVo>> getPredictions(@PathVariable String stockCode) {
        List<Prediction> predictions = predictionService.getPredictionsByStockCode(stockCode);
        List<PredictionVo> predictionVos = predictions.stream()
            .map(this::convertToVo)
            .collect(Collectors.toList());
        return Result.success(predictionVos);
    }

    @GetMapping("/predictions/{stockCode}/summary")
    public Result<PredictionSummaryVo> getPredictionSummary(@PathVariable String stockCode) {
        PredictionSummaryVo summary = predictionService.getPredictionSummary(stockCode);
        return Result.success(summary);
    }

    private PredictionVo convertToVo(Prediction prediction) {
        PredictionVo vo = new PredictionVo();
        BeanUtils.copyProperties(prediction, vo);
        return vo;
    }
}
