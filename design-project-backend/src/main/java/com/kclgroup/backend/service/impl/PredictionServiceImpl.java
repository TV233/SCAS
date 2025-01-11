package com.kclgroup.backend.service.impl;

import com.baomidou.mybatisplus.extension.service.impl.ServiceImpl;
import com.kclgroup.backend.mapper.PredictionMapper;
import com.kclgroup.backend.pojo.entity.Prediction;
import com.kclgroup.backend.pojo.vo.PredictionSummaryVo;
import com.kclgroup.backend.service.PredictionService;
import com.kclgroup.backend.service.StockPricesService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.math.BigDecimal;
import java.math.RoundingMode;
import java.time.LocalDate;
import java.sql.Date;
import java.util.stream.Collectors;
import java.util.Optional;
import java.time.temporal.ChronoUnit;

@Service
public class PredictionServiceImpl extends ServiceImpl<PredictionMapper, Prediction> 
    implements PredictionService {
    
    @Autowired
    private PredictionMapper predictionMapper;
    
    @Autowired
    private StockPricesService stockPricesService;

    @Override
    public List<Prediction> getPredictionsByStockCode(String stockCode) {
        return predictionMapper.getPredictionsByStockCode(stockCode);
    }

    @Override
    public Prediction getLatestPrediction(String stockCode, String modelName) {
        return predictionMapper.getLatestPrediction(stockCode, modelName);
    }

    @Override
    public String getMostAccurateModel(String stockCode) {
        return predictionMapper.getMostAccurateModel(stockCode);
    }

    @Override
    public PredictionSummaryVo getPredictionSummary(String stockCode) {
        PredictionSummaryVo summary = new PredictionSummaryVo();
        String mostAccurateModel = getMostAccurateModel(stockCode);
        summary.setMostAccurateModel(mostAccurateModel);

        if (mostAccurateModel != null) {
            List<Prediction> predictions = predictionMapper.getPredictionsByStockCode(stockCode)
                .stream()
                .filter(p -> p.getModelName().equals(mostAccurateModel))
                .sorted((a, b) -> a.getPredictionDate().compareTo(b.getPredictionDate()))
                .collect(Collectors.toList());

            if (!predictions.isEmpty()) {
                // 使用 StockPricesService 获取当前实际股价
                String latestPriceStr = stockPricesService.getLatestPrice(stockCode);
                BigDecimal currentPrice = new BigDecimal(latestPriceStr);
                
                System.out.println("当前实际股价: " + currentPrice);
                
                // 找到不同时间段的预测
                Prediction weekPrediction = findPredictionForDays(predictions, 7);
                Prediction monthPrediction = findPredictionForDays(predictions, 30);
                Prediction threeMonthPrediction = findPredictionForDays(predictions, 90);

                System.out.println("一周预测: " + (weekPrediction != null ? weekPrediction.getPredictedPrice() : "null"));
                System.out.println("一月预测: " + (monthPrediction != null ? monthPrediction.getPredictedPrice() : "null"));
                System.out.println("三月预测: " + (threeMonthPrediction != null ? threeMonthPrediction.getPredictedPrice() : "null"));

                if (currentPrice != null) {
                    summary.setOneWeekChange(calculateChange(currentPrice, 
                        weekPrediction != null ? weekPrediction.getPredictedPrice() : currentPrice));
                    summary.setOneMonthChange(calculateChange(currentPrice, 
                        monthPrediction != null ? monthPrediction.getPredictedPrice() : currentPrice));
                    summary.setThreeMonthChange(calculateChange(currentPrice, 
                        threeMonthPrediction != null ? threeMonthPrediction.getPredictedPrice() : currentPrice));
                    summary.setModelAccuracy(predictions.get(predictions.size() - 1).getAccuracy());
                }
            }
        }

        return summary;
    }

    private Prediction findPredictionForDays(List<Prediction> predictions, int days) {
        LocalDate currentDate = LocalDate.now();
        LocalDate targetDate = currentDate.plusDays(days);
        
        System.out.println("目标日期: " + targetDate);
        
        // 找到最接近目标日期的预测
        return predictions.stream()
            .filter(p -> p.getPredictionDate() != null)
            .min((a, b) -> {
                // 使用时间戳来比较日期
                long diffA = Math.abs(a.getPredictionDate().getTime() - Date.valueOf(targetDate).getTime());
                long diffB = Math.abs(b.getPredictionDate().getTime() - Date.valueOf(targetDate).getTime());
                return Long.compare(diffA, diffB);
            })
            .orElseGet(() -> predictions.isEmpty() ? null : predictions.get(predictions.size() - 1));
    }

    private BigDecimal calculateChange(BigDecimal currentPrice, BigDecimal predictedPrice) {
        if (currentPrice == null || currentPrice.compareTo(BigDecimal.ZERO) == 0 || predictedPrice == null) {
            return BigDecimal.ZERO;
        }
        
        System.out.println("计算变化幅度 - 当前价格: " + currentPrice + ", 预测价格: " + predictedPrice);
        
        // 计算变化幅度：(预测价格 - 当前价格) / 当前价格
        // 正数表示上涨，负数表示下跌
        return predictedPrice.subtract(currentPrice)
                .divide(currentPrice, 4, RoundingMode.HALF_UP);
    }
}
