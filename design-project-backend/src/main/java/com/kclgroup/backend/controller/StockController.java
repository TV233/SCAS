package com.kclgroup.backend.controller;

import com.kclgroup.backend.pojo.entity.FinancialData;
import com.kclgroup.backend.pojo.entity.Predict;
import com.kclgroup.backend.pojo.entity.Result;
import com.kclgroup.backend.pojo.entity.StockInfo;
import com.kclgroup.backend.pojo.vo.FinancialDataVo;
import com.kclgroup.backend.pojo.vo.StockInfoVo;
import com.kclgroup.backend.service.FinancialDataService;
import com.kclgroup.backend.service.PredictService;
import com.kclgroup.backend.service.StockInfoService;
import com.kclgroup.backend.service.StockPricesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

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
}
