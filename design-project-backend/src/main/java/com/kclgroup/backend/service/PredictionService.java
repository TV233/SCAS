package com.kclgroup.backend.service;

import com.baomidou.mybatisplus.extension.service.IService;
import com.kclgroup.backend.pojo.entity.Prediction;
import com.kclgroup.backend.pojo.vo.PredictionSummaryVo;

import java.util.List;

public interface PredictionService extends IService<Prediction> {
    List<Prediction> getPredictionsByStockCode(String stockCode);
    
    Prediction getLatestPrediction(String stockCode, String modelName);
    
    String getMostAccurateModel(String stockCode);
    
    // 获取预测汇总信息
    PredictionSummaryVo getPredictionSummary(String stockCode);
} 