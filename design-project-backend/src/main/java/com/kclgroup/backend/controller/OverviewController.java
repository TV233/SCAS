package com.kclgroup.backend.controller;

import com.kclgroup.backend.pojo.entity.*;
import com.kclgroup.backend.pojo.vo.*;
import com.kclgroup.backend.service.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api")
@Validated
public class OverviewController {
    @Autowired
    private TopTextService topTextService;
    @Autowired
    private EmotionIndexService emotionIndexService;
    @Autowired
    private SectorsAndStocksService sectorsAndStocksService;
    @Autowired
    private MarketStyleService marketStyleService;
    @Autowired
    private PredictService predictService;
    @Autowired
    private  StockPricesService stockPricesService;
    @Autowired
    private StockIndicesService stockIndicesService;
    @Autowired
    private IndexKlinesService indexKlinesService;

    @GetMapping
    public String overview() {
        return "overview";
    }
    @GetMapping("/top_text")
    public Result<TopText> topText() {
        TopText topText = topTextService.getTopText();
        return Result.success(topText);
    }
    @GetMapping("/emotion_index")
    public Result<EmotionIndex> emotionIndex() {
        EmotionIndex emotionIndex = emotionIndexService.getEmotionIndex();
        return Result.success(emotionIndex);
    }
    @GetMapping("/sectors")
    public Result<List<SectorsAndStocks>> sectors() {
        List<SectorsAndStocks> sectorsAndStocks = sectorsAndStocksService.getSectorsAndStocks();
        return Result.success(sectorsAndStocks);
    }
    @GetMapping("/market_style")
    public Result<List<MarketStyle>> marketStyle() {
        List<MarketStyle> marketStyles = marketStyleService.getMarketStyle();
        return Result.success(marketStyles);
    }

    @GetMapping("/predict")
    public Result<List<PredictVo>> predict() {
        List<PredictVo> predicts = predictService.getPredict();
        return Result.success(predicts);
    }
    @GetMapping("/stock_prices")
    public Result<List<StockPriceVo>> stockPrices() {
        List<StockPriceVo> stockPrices = stockPricesService.getStockPrices();
        return Result.success(stockPrices);
    }

    //上证指数/深证成指/创业板指/沪深300各项数据
    @GetMapping("/stock_indices")
    public  Result<List<StockIndicesVo>> stockIndices() {
        List<StockIndicesVo> stockIndices = stockIndicesService.getStockIndices();
        return Result.success(stockIndices);
    }

    //输入指数代码，返回指数数据
    @GetMapping("/index_klines")
    public Result<List<IndexKlineVo>> indexKlines(@RequestParam String indexCode) {
        List<IndexKlineVo> indexKlines = indexKlinesService.getIndexKlines(indexCode);
        return Result.success(indexKlines);
    }

    @GetMapping("/upDown")
    public Result<PriceVo> upDown() {
        PriceVo priceVo = stockPricesService.getUpDown();
        return Result.success(priceVo);
    }

}
