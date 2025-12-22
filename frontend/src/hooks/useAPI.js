import { useQuery, useMutation, useQueryClient } from 'react-query';
import { queryAPI, weatherAPI, cropsAPI, financeAPI, voiceAPI } from '../services/api';
import toast from 'react-hot-toast';

// Query API hooks
export const useProcessQuery = () => {
  return useMutation(
    (queryData) => queryAPI.processQuery(queryData),
    {
      onError: (error) => {
        toast.error('Failed to process query. Please try again.');
        console.error('Query processing error:', error);
      },
    }
  );
};

export const useProcessVoiceQuery = () => {
  return useMutation(
    ({ audioFile, language, userLocation, userContext }) => 
      queryAPI.processVoiceQuery(audioFile, language, userLocation, userContext),
    {
      onError: (error) => {
        toast.error('Failed to process voice query. Please try again.');
        console.error('Voice query error:', error);
      },
    }
  );
};

export const useProcessImageQuery = () => {
  return useMutation(
    ({ imageFile, queryText, language }) => 
      queryAPI.processImageQuery(imageFile, queryText, language),
    {
      onError: (error) => {
        toast.error('Failed to process image query. Please try again.');
        console.error('Image query error:', error);
      },
    }
  );
};

export const useQueryHistory = (limit = 10, offset = 0) => {
  return useQuery(
    ['queryHistory', limit, offset],
    () => queryAPI.getQueryHistory(limit, offset),
    {
      staleTime: 5 * 60 * 1000, // 5 minutes
      onError: (error) => {
        toast.error('Failed to load query history.');
        console.error('Query history error:', error);
      },
    }
  );
};

export const useSubmitFeedback = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ queryId, rating, feedback }) => queryAPI.submitFeedback(queryId, rating, feedback),
    {
      onSuccess: () => {
        toast.success('Feedback submitted successfully!');
        queryClient.invalidateQueries(['queryHistory']);
      },
      onError: (error) => {
        toast.error('Failed to submit feedback. Please try again.');
        console.error('Feedback submission error:', error);
      },
    }
  );
};

export const useQueryTypes = () => {
  return useQuery(
    ['queryTypes'],
    () => queryAPI.getQueryTypes(),
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        console.error('Query types error:', error);
      },
    }
  );
};

export const useAICapabilities = () => {
  return useQuery(
    ['aiCapabilities'],
    () => queryAPI.getAICapabilities(),
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        console.error('AI capabilities error:', error);
      },
    }
  );
};

// Weather API hooks
export const useCurrentWeather = (latitude, longitude, enabled = true) => {
  return useQuery(
    ['currentWeather', latitude, longitude],
    () => weatherAPI.getCurrentWeather(latitude, longitude),
    {
      enabled: enabled && !!latitude && !!longitude,
      staleTime: 5 * 60 * 1000, // 5 minutes
      onError: (error) => {
        toast.error('Failed to load weather data.');
        console.error('Weather error:', error);
      },
    }
  );
};

export const useWeatherForecast = (latitude, longitude, days = 7, enabled = true) => {
  return useQuery(
    ['weatherForecast', latitude, longitude, days],
    () => weatherAPI.getForecast(latitude, longitude, days),
    {
      enabled: enabled && !!latitude && !!longitude,
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        toast.error('Failed to load weather forecast.');
        console.error('Weather forecast error:', error);
      },
    }
  );
};

export const useWeatherAlerts = (latitude, longitude, enabled = true) => {
  return useQuery(
    ['weatherAlerts', latitude, longitude],
    () => weatherAPI.getAlerts(latitude, longitude),
    {
      enabled: enabled && !!latitude && !!longitude,
      staleTime: 5 * 60 * 1000, // 5 minutes
      onError: (error) => {
        console.error('Weather alerts error:', error);
      },
    }
  );
};

export const useWeatherRecommendations = (latitude, longitude, enabled = true) => {
  return useQuery(
    ['weatherRecommendations', latitude, longitude],
    () => weatherAPI.getRecommendations(latitude, longitude),
    {
      enabled: enabled && !!latitude && !!longitude,
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        console.error('Weather recommendations error:', error);
      },
    }
  );
};

// Crops API hooks
export const useCropRecommendations = (latitude, longitude, temperature, rainfall, humidity, enabled = true) => {
  return useQuery(
    ['cropRecommendations', latitude, longitude, temperature, rainfall, humidity],
    () => cropsAPI.getCropRecommendations(latitude, longitude, temperature, rainfall, humidity),
    {
      enabled: enabled && !!latitude && !!longitude,
      staleTime: 15 * 60 * 1000, // 15 minutes
      onError: (error) => {
        toast.error('Failed to load crop recommendations.');
        console.error('Crop recommendations error:', error);
      },
    }
  );
};

export const useCropManagementAdvice = (cropName, growthStage, latitude, longitude, temperature, rainfall, humidity, enabled = true) => {
  return useQuery(
    ['cropManagementAdvice', cropName, growthStage, latitude, longitude, temperature, rainfall, humidity],
    () => cropsAPI.getCropManagementAdvice(cropName, growthStage, latitude, longitude, temperature, rainfall, humidity),
    {
      enabled: enabled && !!cropName && !!growthStage && !!latitude && !!longitude,
      staleTime: 15 * 60 * 1000, // 15 minutes
      onError: (error) => {
        toast.error('Failed to load crop management advice.');
        console.error('Crop management advice error:', error);
      },
    }
  );
};

export const useCropInfo = (cropName, enabled = true) => {
  return useQuery(
    ['cropInfo', cropName],
    () => cropsAPI.getCropInfo(cropName),
    {
      enabled: enabled && !!cropName,
      staleTime: 30 * 60 * 1000, // 30 minutes
      onError: (error) => {
        console.error('Crop info error:', error);
      },
    }
  );
};

// Finance API hooks
export const useLoanCalculator = (loanAmount, repaymentPeriodMonths, loanType = 'crop_loan', enabled = true) => {
  return useQuery(
    ['loanCalculator', loanAmount, repaymentPeriodMonths, loanType],
    () => financeAPI.getLoanCalculator(loanAmount, repaymentPeriodMonths, loanType),
    {
      enabled: enabled && !!loanAmount && !!repaymentPeriodMonths,
      staleTime: 5 * 60 * 1000, // 5 minutes
      onError: (error) => {
        toast.error('Failed to calculate loan details.');
        console.error('Loan calculator error:', error);
      },
    }
  );
};

export const useMarketTrends = (crop = null) => {
  return useQuery(
    ['marketTrends', crop],
    () => financeAPI.getMarketTrends(crop),
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        toast.error('Failed to load market trends.');
        console.error('Market trends error:', error);
      },
    }
  );
};

export const useFinancialInfo = (state = null, loanAmountNeeded = null, enabled = true) => {
  return useQuery(
    ['financialInfo', state, loanAmountNeeded],
    () => financeAPI.getFinancialInfo(state, loanAmountNeeded),
    {
      enabled: enabled,
      staleTime: 15 * 60 * 1000, // 15 minutes
      onError: (error) => {
        console.error('Financial info error:', error);
      },
    }
  );
};

// Voice API hooks
export const useSpeechToText = () => {
  return useMutation(
    ({ audioFile, language }) => voiceAPI.speechToText(audioFile, language),
    {
      onError: (error) => {
        toast.error('Failed to convert speech to text.');
        console.error('Speech to text error:', error);
      },
    }
  );
};

export const useTextToSpeech = () => {
  return useMutation(
    ({ text, language }) => voiceAPI.textToSpeech(text, language),
    {
      onError: (error) => {
        toast.error('Failed to convert text to speech.');
        console.error('Text to speech error:', error);
      },
    }
  );
};

export const useDetectLanguage = () => {
  return useMutation(
    (text) => voiceAPI.detectLanguage(text),
    {
      onError: (error) => {
        console.error('Language detection error:', error);
      },
    }
  );
};

export const useLanguages = () => {
  return useQuery(
    ['languages'],
    () => voiceAPI.getLanguages(),
    {
      staleTime: 30 * 60 * 1000, // 30 minutes
      onError: (error) => {
        console.error('Languages error:', error);
      },
    }
  );
};

export const useValidateAudio = () => {
  return useMutation(
    (audioFile) => voiceAPI.validateAudio(audioFile),
    {
      onError: (error) => {
        toast.error('Failed to validate audio file.');
        console.error('Audio validation error:', error);
      },
    }
  );
};

export const useVoiceSettings = () => {
  return useQuery(
    ['voiceSettings'],
    () => voiceAPI.getSettings(),
    {
      staleTime: 10 * 60 * 1000, // 10 minutes
      onError: (error) => {
        console.error('Voice settings error:', error);
      },
    }
  );
}; 